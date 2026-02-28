import math, time, sys, array

try:
    import shutil
    W, H = shutil.get_terminal_size((80, 24))
    H -= 1
except:
    W, H = 80, 23

CX, CY = W // 2, H // 2
GRAD = " .,-~:;=!*#$@█▓▒░"

def render(A, B, C, t):
    size   = W * H
    screen = [' '] * size
    zbuf   = [0.0]  * size

    sA, cA = math.sin(A), math.cos(A)
    sB, cB = math.sin(B), math.cos(B)
    sC, cC = math.sin(C), math.cos(C)

    pulse = 1.0 + 0.15 * math.sin(t * 3.1)
    R1 = 1.0 * pulse
    R2 = 2.0

    #light
    lx = math.cos(t * 0.8)
    ly = math.sin(t * 0.5)
    lz = math.sin(t * 0.35) - 2.0
    ll = math.sqrt(lx*lx + ly*ly + lz*lz)
    lx /= ll; ly /= ll; lz /= ll

    TSTEP = 0.06
    PSTEP = 0.022

    theta = 0.0
    while theta < 6.2832:
        ct = math.cos(theta); st = math.sin(theta)
        phi = 0.0
        while phi < 6.2832:
            cp = math.cos(phi); sp = math.sin(phi)

            #torus point
            ox = (R2 + R1*ct)*cp
            oy = (R2 + R1*ct)*sp
            oz =  R1*st
            nx = ct*cp; ny = ct*sp; nz = st
            ox,oz = ox*cC+oz*sC, -ox*sC+oz*cC
            nx,nz = nx*cC+nz*sC, -nx*sC+nz*cC
            oy,oz = oy*cA-oz*sA, oy*sA+oz*cA
            ny,nz = ny*cA-nz*sA, ny*sA+nz*cA

            ox,oy = ox*cB-oy*sB, ox*sB+oy*cB
            nx,ny = nx*cB-ny*sB, nx*sB+ny*cB

            z = oz + 5.0
            if z < 0.1:
                phi += PSTEP; continue

            inv_z = 1.0 / z
            sc = min(W, H*2) * 0.43

            xp = int(CX + sc*ox*inv_z)
            yp = int(CY + sc*oy*inv_z*0.55)

            if 0 <= xp < W and 0 <= yp < H:
                idx = xp + W*yp
                if inv_z > zbuf[idx]:
                    zbuf[idx] = inv_z

                    diff = nx*lx + ny*ly + nz*lz
                    ndl2 = 2*diff
                    spec = max(0.0, -(ndl2*nz - lz))**8
                    rim  = (1.0 - abs(nz))**3 * 0.35
                    lum  = min(1.0, 0.12 + 0.55*max(0.0,diff) + 0.33*spec + rim)

                    ci = int(lum * (len(GRAD)-1))
                    screen[idx] = GRAD[ci]

            phi += PSTEP
        theta += TSTEP

    lines = []
    for r in range(H):
        lines.append("".join(screen[r*W:(r+1)*W]))
    return "\n".join(lines)


def main():
    A = B = 0.0
    dA, dB = 0.07, 0.05
    t = 0.0
    FT = 1.0 / 25  #25 fps

    sys.stdout.write("\033[2J\033[?25l")
    sys.stdout.flush()
    try:
        while True:
            t0 = time.perf_counter()
            C = 0.45 * math.sin(t * 0.38) 
            sys.stdout.write("\033[H" + render(A, B, C, t))
            sys.stdout.flush()
            A += dA; B += dB; t += FT
            wait = FT - (time.perf_counter() - t0)
            if wait > 0: time.sleep(wait)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\n"); sys.stdout.flush()

if __name__ == "__main__":
    main()
