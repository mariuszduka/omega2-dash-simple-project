#
# Initalize touch screen
#
def initDisplay(width = 320, height = 240, touch = True):
	# LittelvGL
	# https://docs.lvgl.io/latest/en/html/index.html
	import lvgl as lv
	lv.init()
	
	# Linux Frame Buffer
	import fb
	fb.init()

	# Register display driver.
	disp_buf1 = lv.disp_buf_t()
	buf1_1 = bytearray(320*10)
	lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1)//4)
	
	disp_drv = lv.disp_drv_t()
	lv.disp_drv_init(disp_drv)
	disp_drv.buffer = disp_buf1
	disp_drv.flush_cb = fb.flush
	disp_drv.hor_res = width
	disp_drv.ver_res = height
	lv.disp_drv_register(disp_drv)
	
	if touch == True:
		import xpt7603
		touch = xpt7603.xpt7603()
		touch.init()
	
		indev_drv = lv.indev_drv_t()
		lv.indev_drv_init(indev_drv) 
		indev_drv.type = lv.INDEV_TYPE.POINTER
		indev_drv.read_cb = touch.read
		lv.indev_drv_register(indev_drv)
	
	return lv