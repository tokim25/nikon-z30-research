/* Auto-arm (research SD module for the Wonder Lantern module host).
 *
 * Goal (owner, 2026-11-17): on the shooting screen in Auto-area AF the camera
 * sits in the tracking-ready screen (the reticle OK brings up) without any
 * button press, so a half-press starts tracking and upstream's 3D tracking
 * can hand it to a face or animal. No button is remapped. When tracking ends
 * or the user backs out, the module brings the reticle back right away.
 *
 * It sends one OK press when all of these hold on an IMU tick:
 *   - shooting screen: UI phase byte 0xC181F6FC is 1 or 2 (upstream's
 *     3d-tracking box drawing uses this check);
 *   - Auto-area AF: AF-area mode byte 0xC237C7F8 is 6 (upstream PR #36 rev 6);
 *   - idle: 0xC237F680 (AF working: tracking or half-press), 0xC237F684
 *     (tracking box shown, screen 1) and 0xC237F688 (tracking) are all 0
 *     (upstream af-tracking-research, camera logs);
 *   - those held for SETTLE consecutive ticks, and no OK is still pending.
 * After a press it waits until the tracking box shows or WAIT ticks pass.
 *
 * Pieces reused from upstream, run on a Z30 C 1.20 (PR #36):
 *   - the IMU-task hook cell 0xC1832D48 (imu_hook, about every 50 ms), which
 *     builds together with 3d-tracking (tools/build_af_log.py --module log);
 *   - the input ring 0xC2008EA0 (16 x 0x190; next slot in 0xC182004C) and the
 *     v6 OK press made from the IMU task: copy the newest real entry, set every
 *     key word (+4 / +0x18 / +0x2C / +0x40: cur, prev, changed, pressed,
 *     released) to "no change" except key word 2 bit 0 (OK), and pass it to
 *     0x102F0D14 then 0x102F1844, once down and once up.
 *
 * Unverified: that the phase byte is not 1/2 while the i menu or another
 * overlay is open, and that an OK sent at live-view entry is accepted. Build
 * without -DREMAP first: it logs every tick on which it would press, with the
 * state bytes, and presses nothing.
 *
 * Run 1: arm.  Run 2: disarm and write A:\Z30\ARnnnnnn.BIN.  Power off disarms.
 * File: "AUTOARM1", u32 count, u32 presses, u32 ticks, u32 rec_bytes (12),
 *       u32 flags (bit 0 = REMAP build), u32 0, then count x rec.
 */
#include <stdint.h>
#include "z30_module_api.h"

typedef void *(*pool_alloc_fn)(uint32_t size, uint32_t flags);
#define POOL_ALLOC ((pool_alloc_fn)0x10211F4Du)
typedef int32_t (*fs_open_fn)(const char *path, uint32_t flags);
#define FS_OPEN   ((fs_open_fn)0x102C8AFDu)
typedef int32_t (*fs_write_fn)(int32_t fd, const void *buf, uint32_t len, uint32_t *done);
#define FS_WRITE  ((fs_write_fn)0x102C8A6Bu)
typedef int32_t (*fs_close_fn)(int32_t fd);
#define FS_CLOSE  ((fs_close_fn)0x102C89EFu)
typedef int32_t (*range_fn)(uint32_t addr, uint32_t len, uint32_t op, uint32_t scope);
#define RANGE_SERVICE ((range_fn)0x10035AACu)
typedef int32_t (*input_fn)(void *state);
#define INPUT_PUT  ((input_fn)0x102F0D15u)
#define INPUT_POST ((input_fn)0x102F1845u)
typedef void (*time_fn)(uint64_t *out);
#define TIME_US ((time_fn)0x101D8301u)

#define HOOK_CELL ((volatile uint32_t *)0xC1832D48u)   /* imu_hook */
#define UI_PHASE ((const volatile uint8_t *)0xC181F6FCu)
#define AF_AREA ((const volatile uint8_t *)0xC237C7F8u)
#define AUTO_AREA 6u
#define AF_BUSY 0xC237F680u
#define BOX_SHOWN 0xC237F684u
#define TRACKING 0xC237F688u
#define RING 0xC2008EA0u
#define RING_IDX 0xC182004Cu
#define RING_STRIDE 0x190u
#define STATE_BYTES 0x18Cu
#define OK_BIT 0x1u                     /* key word 2 */
#define SETTLE 2u                       /* idle ticks before a press (~100 ms) */
#define WAIT 30u                        /* ticks to wait for the box (~1.5 s) */
#define RD(a) (*(const volatile uint32_t *)(a))

struct rec {                            /* 12 bytes, one per (would-be) press */
    uint32_t t_ms;
    uint8_t phase, area, flags, pad;    /* flags: bit 0 OK sent, bits 2-3 writer results */
    uint32_t pad2;
};
_Static_assert(sizeof(struct rec) == 12, "rec");
#define HDR 32u
#define CAP 8192u
#define POOL_BYTES (HDR + CAP * sizeof(struct rec))

void *memcpy(void *d, const void *s, uint32_t n)
{ uint8_t *a = d; const uint8_t *b = s; while (n--) *a++ = *b++; return d; }
void *memset(void *d, int v, uint32_t n)
{ uint8_t *a = d; while (n--) *a++ = (uint8_t)v; return d; }

static inline void barrier(void) { __asm__ volatile("dmb" ::: "memory"); }
static uint64_t time_us(void) { uint64_t t = 0; TIME_US(&t); return t; }

static struct {
    uint8_t *pool; struct rec *log;
    uint32_t count, ticks, presses, idle_run, waiting, file_no, held[4], state[STATE_BYTES / 4];
    uint64_t t0;
    volatile uint32_t on, busy;
} G;

struct context { uint32_t runs, pad; char text[40]; };

#ifdef REMAP
static void key_word(uint32_t *f, uint32_t cur, uint32_t prev)
{
    uint32_t ch = cur ^ prev;
    f[0] = cur; f[1] = prev; f[2] = ch; f[3] = cur & ch; f[4] = prev & ch;
}

/* Upstream v6: a copy of the entry at src, nothing changing except OK. */
static uint32_t press_ok(uint32_t src, int down)
{
    uint32_t *st = G.state;
    for (uint32_t i = 0; i < STATE_BYTES / 4u; i++) st[i] = RD(src + 4u * i);
    for (uint32_t w = 0; w < 4; w++) key_word(&st[1 + 5 * w], G.held[w], G.held[w]);
    if (down) key_word(&st[6], G.held[1] | OK_BIT, G.held[1]);
    else key_word(&st[6], G.held[1], G.held[1] | OK_BIT);
    if (!INPUT_PUT(st)) return 0;
    INPUT_POST(st);
    return 1;
}
#endif

static void tick(uint32_t stock_result)
{
    (void)stock_result;                 /* the stock accel read; never changed */
    G.busy = 1; barrier();
    if (!G.on) goto out;
    G.ticks++;
    uint32_t phase = *UI_PHASE, area = *AF_AREA, shown = RD(BOX_SHOWN);
    if (G.waiting) {                    /* an OK was sent: let it land */
        if (shown || --G.waiting == 0) G.waiting = 0;
        G.idle_run = 0;
        goto out;
    }
    int idle = (phase == 1u || phase == 2u) && area == AUTO_AREA &&
               !RD(AF_BUSY) && !shown && !RD(TRACKING);
    G.idle_run = idle ? G.idle_run + 1u : 0u;
    if (G.idle_run < SETTLE) goto out;
    G.idle_run = 0;
    struct rec scratch, *r = G.count < CAP ? &G.log[G.count++] : &scratch;
    r->t_ms = (uint32_t)((time_us() - G.t0) / 1000u);
    r->phase = (uint8_t)phase; r->area = (uint8_t)area; r->flags = 0; r->pad = 0; r->pad2 = 0;
    G.presses++;
    G.waiting = WAIT;
#ifdef REMAP
    uint32_t newest = RING + ((RD(RING_IDX) - 1u) & 0xFu) * RING_STRIDE;
    G.held[0] = RD(newest + 4); G.held[1] = RD(newest + 0x18) & ~OK_BIT;
    G.held[2] = RD(newest + 0x2C); G.held[3] = RD(newest + 0x40);
    uint32_t down = press_ok(newest, 1), up = press_ok(newest, 0);
    r->flags = (uint8_t)(1u | down << 2 | up << 3);
#endif
out:
    barrier(); G.busy = 0;
}

static int shared_clean(const void *p, uint32_t n)
{
    volatile uint32_t *smp = (volatile uint32_t *)0xC2ABC8B8u;
    if (smp[0] != 1 || *(volatile uint32_t *)0xC18EB038u != 2 || smp[5] != 3 || smp[1] != 1 ||
        *(volatile uint32_t *)0xC2A1C7F0u != 0x100527A8u || !n)
        return 0;
    uint32_t a = (uint32_t)p & ~63u;
    n += (uint32_t)p - a;
    if (RANGE_SERVICE(a, n, 1, 2) <= 0) return 0;
    __asm__ volatile("dsb" ::: "memory");
    return 1;
}

static int write_all(int32_t fd, const uint8_t *p, uint32_t n)
{
    while (n) {
        uint32_t chunk = n > 65536u ? 65536u : n, done = 0;
        FS_WRITE(fd, p, chunk, &done);
        if (done == 0 || done > chunk) return 0;
        p += done; n -= done;
    }
    return 1;
}

static void put_u(char **p, uint32_t v)
{ char b[10]; int n = 0; do { b[n++] = (char)('0' + v % 10u); v /= 10u; } while (v); while (n) *(*p)++ = b[--n]; }
static void put_s(char **p, const char *s) { while (*s) *(*p)++ = *s++; }

static uint32_t say(const struct z30_module_api *api, struct context *c, const char *a, uint32_t n, int num)
{
    char *p = c->text;
    put_s(&p, a); if (num) put_u(&p, n); *p = 0;
    return api->set_text(c->text);
}

static uint32_t save(const struct z30_module_api *api, struct context *c)
{
    G.on = 0; barrier();
    for (uint32_t spin = 0; G.busy && spin < 50000000u; spin++) barrier();
    if (G.busy) return say(api, c, "Busy, Run again", 0, 0);
#ifdef REMAP
    uint32_t flags = 1;
#else
    uint32_t flags = 0;
#endif
    uint32_t h[8] = { 0x4F545541u, 0x314D5241u, G.count, G.presses, G.ticks, sizeof(struct rec), flags, 0 };
    memcpy(G.pool, h, HDR);
    char path[24] = "A:\\Z30\\AR000000.BIN";
    uint32_t sec = (uint32_t)(time_us() / 1000000u) + G.file_no++;
    for (int i = 14; i >= 9; i--) { path[i] = (char)('0' + sec % 10u); sec /= 10u; }
    uint32_t bytes = HDR + G.count * sizeof(struct rec);
    shared_clean(G.pool, bytes);
    int32_t fd = FS_OPEN(path, 0x20);
    int ok = fd >= 0 && write_all(fd, G.pool, bytes);
    if (fd >= 0) FS_CLOSE(fd);
    if (!ok) return say(api, c, "Save failed ", (uint32_t)fd, 1);
    return say(api, c, "Saved, presses ", G.presses, 1);
}

static uint32_t module_run(const struct z30_module_api *api, void *vctx)
{
    struct context *c = vctx;
    c->runs++;
    if (!G.pool) {
        G.pool = POOL_ALLOC(POOL_BYTES, 0);
        if (!G.pool) return say(api, c, "No memory", 0, 0);
        G.log = (struct rec *)(G.pool + HDR);
    }
    if (G.on) return save(api, c);
    if (*HOOK_CELL && *HOOK_CELL != (uint32_t)tick) return say(api, c, "IMU hook in use", 0, 0);
    G.count = G.ticks = G.presses = G.idle_run = G.waiting = 0; G.t0 = time_us();
    barrier();
    *HOOK_CELL = (uint32_t)tick;
    G.on = 1; barrier();
#ifdef REMAP
    return say(api, c, "Auto-arm on, Run=save", 0, 0);
#else
    return say(api, c, "Auto-arm dry run, Run=save", 0, 0);
#endif
}

__attribute__((section(".text.entry"), used))
uint32_t module_init(const struct z30_module_api *api, void *ctx)
{
    struct context *c = ctx;
    char *p = c->text; put_s(&p, "Auto-arm ready"); *p = 0;
    api->set_text(c->text);
    return api->set_run_handler(module_run);
}
