#!/usr/bin/env python3
import struct, zlib, base64

def make_png(size, bg, symbol_color):
    w, h = size, size
    raw = []
    cx, cy = w//2, h//2
    r = int(w * 0.28)
    br = int(w * 0.18)
    
    for y in range(h):
        row = []
        for x in range(w):
            # Rounded rect background
            dx = abs(x - cx)
            dy = abs(y - cy)
            in_bg = dx <= (cx - br) or dy <= (cy - br) or ((dx - (cx - br))**2 + (dy - (cy - br))**2) <= br**2
            
            if in_bg:
                # Draw a simple "$" like symbol - white circle outline
                dist = ((x-cx)**2 + (y-cy)**2)**0.5
                # Vertical line
                if abs(x - cx) <= w*0.04 and abs(y - cy) <= h*0.22:
                    row += [255, 255, 255, 255]
                # Top arc
                elif abs(dist - r*0.6) < w*0.04 and y < cy and x >= cx - r*0.5 and x <= cx + r*0.5:
                    row += [255, 255, 255, 255]
                # Bottom arc  
                elif abs(dist - r*0.6) < w*0.04 and y > cy and x >= cx - r*0.5 and x <= cx + r*0.5:
                    row += [255, 255, 255, 255]
                # Middle bar
                elif abs(y - cy) <= w*0.035 and abs(x - cx) <= r*0.55:
                    row += [255, 255, 255, 255]
                else:
                    row += list(bg) + [255]
            else:
                row += [0, 0, 0, 0]
        raw.append(b'\x00' + bytes(row))
    
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    idat = zlib.compress(b''.join(raw))
    
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

bg = (26, 26, 46)
sc = (212, 175, 55)

with open('icon-192.png', 'wb') as f:
    f.write(make_png(192, bg, sc))

with open('icon-512.png', 'wb') as f:
    f.write(make_png(512, bg, sc))

print("Iconos generados")
