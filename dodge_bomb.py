import time
import os
import random
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650

DELTA = {#移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：判定結果タプル（横方向判断結果、縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """

    yoko,tate = True,True

    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    
    return yoko,tate


def gameover(screen: pg.Surface) -> None:
    go_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(go_img,(0,0,0),(0,0,WIDTH,HEIGHT))
    go_img.set_alpha(150)
    

    go_fnt = pg.font.Font(None,60)
    txt = go_fnt.render("Game Over",True,(255,255,255))
    go_img.blit(txt,[450,300])
    
    

    screen.blit(go_img,(0,0))

    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    right_rct = kk2_img.get_rect(center=(700,310))
    left_rct = kk2_img.get_rect(center = (430,310))
    screen.blit(kk2_img,right_rct)
    screen.blit(kk2_img,left_rct)

    pg.display.update()
    time.sleep(5)


def init_bb_images() -> tuple[list[pg.Surface],list[int]]:
    bb_imgs = []

    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img,(225,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1,11)]

    return bb_imgs,bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)#横初期座標
    bb_rct.centery = random.randint(0,HEIGHT)#縦初期座標
    bb_img.set_colorkey((0,0,0))

    vx,vy = +5,+5

    bb_imgs,bb_accs = init_bb_images()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        

        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key,mv in DELTA.items():
            if key_lst[key]:
             sum_mv[0] += mv[0] #横方向の移動量
             sum_mv[1] += mv[1] #縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1]) #動きをなかったことにする
        screen.blit(kk_img, kk_rct)

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        
        bb_rct.move_ip(avx,avy)
        yoko,tate =  check_bound(bb_rct)
        if not yoko:#横方向にはみ出たら
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
