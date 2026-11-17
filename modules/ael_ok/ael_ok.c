/* AE-L/AF-L to OK (research SD module for the Wonder Lantern module host).
 *
 * Goal: one press of AE-L/AF-L behaves like one press of OK. In Auto-area AF
 * the stock OK starts Subject tracking (reticle; half-press acquires; OK again
 * ends), which is the behavior the owner measured for Fn1 = Subject tracking
 * (F-261). This module reuses only pieces that Wonder Lantern has run on a
 * Z30 C 1.20 (upstream PR #36, docs/af-tracking-research.md):
 *
 *   - the detection-result hook cell 0xC1832D40 (face_hook at 0x101944B0,
 *     called about 10-20 times a second in live view);
 *   - the input ring 0xC2008EA0 (16 entries of 0x190 bytes; next write slot
 *     in the low bits of 0xC182004C). Each entry holds four key words at +4,
 *     +0x18, +0x2C, +0x40, each as cur, prev, changed, pressed, released;
 *   - the v6 OK synthesis: copy the newest real entry, set every key word to
 *     "no change" except key word 2 bit 0 (OK), and pass it to the stock input
 *     writer 0x102F0D14 then 0x102F1844, once down and once up.
 *
 * The OK is sent only when the AF-area mode byte 0xC237C7F8 is 6 (Auto-area),
 * read the way upstream PR #36 revision 6 reads it (stock 0x1039CC14); in
 * other modes the stock OK does other things (zoom by default). This is the
 * field F-339 traces into snapshot +0x44.
 *
 * Unverified, and the reason the log exists: that AE-L/AF-L appears as bit
 * 0x2000 of key word 1. This repository maps mask 0x2000 to logical input 13,
 * "AE-L/AF-L button" (F-229), and reads it at record +4 (F-227); upstream
 * reads key word 1 at the same offset. Build without -DREMAP first, press
 * AE-L/AF-L a counted number of times, and check the log.
 *
 * Run 1: arm.  Run 2: disarm and write A:\Z30\AEnnnnnn.BIN.  Power off disarms.
 * File: "AELOK1\0\0", u32 count, u32 ael_presses, u32 ok_presses, u32 ticks,
 *       u32 rec_bytes (24), u32 flags (bit 0 = REMAP build), then count x rec.
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

#define FACE_CELL ((volatile uint32_t *)0xC1832D40u)
#define RING 0xC2008EA0u
#define RING_IDX 0xC182004Cu
#define RING_N 16u
#define RING_STRIDE 0x190u
#define STATE_BYTES 0x18Cu
#define AEL_BIT 0x2000u                 /* key word 1, inferred (F-227, F-229) */
#define OK_BIT 0x1u                     /* key word 2, upstream camera-verified */
#define AF_AREA ((const volatile uint8_t *)0xC237C7F8u)   /* AF display block +0x44 */
#define AUTO_AREA 6u
#define RD(a) (*(const volatile uint32_t *)(a))

struct rec {                            /* 24 bytes, one per new real ring entry */
    uint32_t t_ms;
    uint8_t slot, flags, area, pad;     /* flags: bit 0 AE-L pressed, bit 1 OK sent, bits 2-3 writer results; area: AF-area mode */
    uint32_t kw1_cur, kw1_pressed, kw2_cur, kw2_pressed;
};
_Static_assert(sizeof(struct rec) == 24, "rec");
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
    uint32_t count, ticks, ael, oks, last, primed, file_no, held[4], state[STATE_BYTES / 4];
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

static uint32_t ms(void) { return (uint32_t)((time_us() - G.t0) / 1000u); }

static void tick(const void *result, const int16_t *xy, const int16_t *wh)
{
    (void)result; (void)xy; (void)wh;
    G.busy = 1; barrier();
    if (!G.on) goto out;
    G.ticks++;
    uint32_t idx = RD(RING_IDX) & 0xFu;
    if (!G.primed) { G.last = idx; G.primed = 1; goto out; }
    struct rec *press = 0;
    for (uint32_t s = G.last; s != idx; s = (s + 1u) & 0xFu) {
        uint32_t e = RING + s * RING_STRIDE;
        uint32_t pressed = RD(e + 0x10);
        struct rec scratch, *r = G.count < CAP ? &G.log[G.count++] : &scratch;
        r->t_ms = ms(); r->slot = (uint8_t)s; r->area = *AF_AREA; r->pad = 0;
        r->flags = pressed & AEL_BIT ? 1u : 0u;
        r->kw1_cur = RD(e + 4); r->kw1_pressed = pressed;
        r->kw2_cur = RD(e + 0x18); r->kw2_pressed = RD(e + 0x24);
        if (r->flags & 1u) { G.ael++; if (r != &scratch) press = r; }
    }
    G.last = idx;
#ifdef REMAP
    if (press && press->area == AUTO_AREA) {   /* one OK per tick, Auto-area AF only */
        uint32_t newest = RING + ((idx - 1u) & 0xFu) * RING_STRIDE;
        G.held[0] = RD(newest + 4); G.held[1] = RD(newest + 0x18) & ~OK_BIT;
        G.held[2] = RD(newest + 0x2C); G.held[3] = RD(newest + 0x40);
        uint32_t down = press_ok(newest, 1), up = press_ok(newest, 0);
        press->flags |= (uint8_t)(2u | down << 2 | up << 3);
        G.oks++;
        G.last = RD(RING_IDX) & 0xFu;   /* skip the two entries just written */
    }
#else
    (void)press;
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
    uint32_t h[8] = { 0x4F4C4541u, 0x0000314Bu, G.count, G.ael, G.oks, G.ticks, sizeof(struct rec), flags };
    memcpy(G.pool, h, HDR);
    char path[24] = "A:\\Z30\\AE000000.BIN";
    uint32_t sec = (uint32_t)(time_us() / 1000000u) + G.file_no++;
    for (int i = 14; i >= 9; i--) { path[i] = (char)('0' + sec % 10u); sec /= 10u; }
    uint32_t bytes = HDR + G.count * sizeof(struct rec);
    shared_clean(G.pool, bytes);
    int32_t fd = FS_OPEN(path, 0x20);
    int ok = fd >= 0 && write_all(fd, G.pool, bytes);
    if (fd >= 0) FS_CLOSE(fd);
    if (!ok) return say(api, c, "Save failed ", (uint32_t)fd, 1);
    return say(api, c, "Saved, AE-L presses ", G.ael, 1);
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
    if (*FACE_CELL && *FACE_CELL != (uint32_t)tick) return say(api, c, "Detection hook in use", 0, 0);
    G.count = G.ticks = G.ael = G.oks = G.primed = 0; G.t0 = time_us();
    barrier();
    *FACE_CELL = (uint32_t)tick;
    G.on = 1; barrier();
#ifdef REMAP
    return say(api, c, "AE-L to OK armed, Run=save", 0, 0);
#else
    return say(api, c, "AE-L log armed, Run=save", 0, 0);
#endif
}

__attribute__((section(".text.entry"), used))
uint32_t module_init(const struct z30_module_api *api, void *ctx)
{
    struct context *c = ctx;
    char *p = c->text; put_s(&p, "AE-L to OK ready"); *p = 0;
    api->set_text(c->text);
    return api->set_run_handler(module_run);
}
