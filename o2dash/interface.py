from display import *
from nfc import checkUID
from remote import *

# Initalize screen
lv = initDisplay()
scr = lv.obj()

admin = False
passwd = "Omega2"
criticalTemp = 30

def mainWindow():	
	theme = lv.theme_night_init(250, lv.font_t.cast(None))
	lv.theme_set_current(theme)
	
	style1 = lv.style_t()
	lv.style_copy(style1, lv.style_plain_color)
	style1.body.main_color = lv.color_hex(0x123456)
	style1.text.color = lv.color_hex(0xFFFFFF)
	style1.text.font = lv.font_roboto_16
	
	win = lv.win(scr)
	win.set_title(" Omega2 Dash Simple Project")
	# win.set_style(lv.win.STYLE.HEADER, style1)
	win.set_btn_size(50)
	
	def on_refresh_btn(obj, event):
		print('on_refresh_btn event')
		if event == lv.EVENT.CLICKED:
			refreshRemote()
			print('refresh_btn clicked!')

	def on_settings_btn(obj, event):
		print('on_settings_btn event')
		if event == lv.EVENT.CLICKED:
			print('settings_btn clicked!')
			checkAccessAdmin()
	
	refresh_btn = win.add_btn(lv.SYMBOL.REFRESH)
	refresh_btn.set_event_cb(on_refresh_btn)
	settings_btn = win.add_btn(lv.SYMBOL.SETTINGS)
	settings_btn.set_event_cb(on_settings_btn)

	return [lv, scr]

def showSensors(temp = 0, relayStatus = True, relayAuto = False):
	mainWindow()

	label1 = lv.label(scr)
	label1.set_recolor(True)
	label1.set_text("#FFFFFF Temperature")
	label1.align(None, lv.ALIGN.CENTER, -55 if admin == True else 0, -45)

	style = lv.style_t()
	lv.style_copy(style, lv.style_pretty_color)
	style.line.color = lv.color_hex3(0xF00)
	style.line.width = 3
	
	needle_colors = [
    	lv.color_make(0xFF, 0xA5, 0x00)
	]

	gauge1 = lv.gauge(scr)
	gauge1.set_range(0, 40)
	gauge1.set_critical_value(criticalTemp)
	gauge1.set_style(lv.gauge.STYLE.MAIN, style)
	gauge1.set_needle_count(len(needle_colors), needle_colors)
	gauge1.set_size(150, 150)
	gauge1.align(None, lv.ALIGN.CENTER, -55 if admin == True else 0, 50)

	gauge1.set_value(0, temp)

	if admin == True:		
		def event_handler_sw1(obj, event):
			if event == lv.EVENT.VALUE_CHANGED:
				if obj.get_state() == True:
					if switchRelay('auto-switch-on') == True:
						print("Done!")
					
					refreshRemote()
					print("ON")
				else:
					if switchRelay('auto-switch-off') == True:
						print("Done!")
					
					refreshRemote()
					print("OFF")
					
		def event_handler_sw2(obj, event):
			if event == lv.EVENT.VALUE_CHANGED:
				if obj.get_state() == True:
					if switchRelay('relay-on') == True:
						print("Done!")
					
					refreshRemote()
					print("ON")
				else:
					if switchRelay('relay-off') == True:
						print("Done!")
					
					refreshRemote()
					print("OFF")
				
		label2 = lv.label(scr)
		label2.set_recolor(True)
		label2.set_text("#FFFFFF Auto Relay")
		label2.align(None, lv.ALIGN.CENTER, 95, -45)
	
		sw1 = lv.sw(scr)
		if relayAuto == True:
			sw1.on(lv.ANIM.ON)
		sw1.align(None, lv.ALIGN.CENTER, 95, -5)
		sw1.set_event_cb(event_handler_sw1)
		
		if relayAuto == False:
			label3 = lv.label(scr)
			label3.set_recolor(True)
			label3.set_text("#FFFFFF Switch Relay")
			label3.align(None, lv.ALIGN.CENTER, 95, 40)
		
			sw2 = lv.sw(scr)
			if relayStatus == True:
				sw2.on(lv.ANIM.ON)
			sw2.align(None, lv.ALIGN.CENTER, 95, 80)
			sw2.set_event_cb(event_handler_sw2)		
		
		label4 = lv.label(scr)
		label4.set_recolor(True)
		label4.set_text("#228B22 Logged in")
		label4.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, -10)

def checkAccessAdmin():
	def event_handler(obj, event):
		if event == lv.EVENT.VALUE_CHANGED:
			print("Button: %s" % lv.mbox.get_active_btn_text(obj))
			
			if (lv.mbox.get_active_btn_text(obj) == "KEY"):
				mbox1.start_auto_close(0)
				checkPassword()
			
			if (lv.mbox.get_active_btn_text(obj) == "NFC"):
				if (checkUID(5) == True):
					mbox1.start_auto_close(0)
					accessAdmin(True)

			if (lv.mbox.get_active_btn_text(obj) == "Close"):
				mbox1.start_auto_close(0)
				
			if (lv.mbox.get_active_btn_text(obj) == "Logout"):
				mbox1.start_auto_close(0)
				accessAdmin(False)
				
			#autoRefresh = True

	if admin == True:
		btns = ["Logout", "Close", ""]
		msg = "You are logged in to the system."
	else:
		btns = ["KEY", "NFC", "Close", ""]
		msg = "Enter password or use registered NFC card to access to the system."
	
	mbox1 = lv.mbox(lv.scr_act())
	mbox1.set_text(msg)
	mbox1.add_btns(btns)
	mbox1.set_width(200)
	mbox1.set_event_cb(event_handler)
	mbox1.align(None, lv.ALIGN.CENTER, 0, 0)
	mbox1.start_auto_close(5000)
	
def checkPassword():
	def event_handler(obj, event):
		# Call original event handler
		obj.def_event_cb(event)
		
		if event == lv.EVENT.APPLY:
			o = kb.get_ta()
			if o.get_text() == passwd:
				accessAdmin(True)
			else:
				refreshRemote()
			print("Apply")	
		if event == lv.EVENT.CANCEL:
			refreshRemote()
			print("Cancel")	
	
	kb = lv.kb(scr)
	kb.set_cursor_manage(True)
	kb.set_style(lv.kb.STYLE.BG, lv.style_transp_tight)
	kb.set_event_cb(event_handler)
	
	ta = lv.ta(scr)
	ta.set_size(250,100)
	ta.align(None, lv.ALIGN.IN_TOP_MID, 0, 10)
	ta.set_text("")
	
	kb.set_ta(ta)	

def accessAdmin(access = False):
	global admin
	
	admin = access
	refreshRemote()
	
def refreshRemote():
	(temp, relayStatus, relayAuto) = checkRemote()
	showSensors(temp, relayStatus, relayAuto)