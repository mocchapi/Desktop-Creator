import configparser
from ast import literal_eval

print('-------------------------------------------------------------------------------')
print('Desktop Creator v1.0  // made by Anne Mocha // MIT license')
print('-------------------------------------------------------------------------------')

try:
	from appJar import gui
except BaseException as e:
	print('FATAL ERROR: appJar cannot be imported and the application cannot be started.')
	print(f'Exact exception: {e}')
	print('-------------------------------------------------------------------------------')
	print('If you are running this program as a stand-alone executable, try checking for updates at the github release page.')
	print('If there are no new updates, please open an issue on the github issues page.')
	print('You could also download the source code and run the desktop-creator.py found within and following the instructions in the next section.')
	print('The source code can be obtained at the github releases page, or by cloning the repository.')
	print('This is the github project page: "https://github.com/mocchapi/Desktop-Creator"')
	print('-------------------------------------------------------------------------------')
	print('If you are running this program using the desktop-creator.py with python 3, try the following:')
	print('Possible solution: Install the "appJar" package using "pip3 install appJar"')
	print('Possible solution: If appJar is installed and you are running this as root, and it works without root, try installing appJar under root instead of the current user by typing "sudo pip3 install appJar"')
	exit()


def ui(app):
	app.setSticky('n')
	app.setStretch('none')
	app.addLabel('label_title','.desktop creator',0,0)
	app.addHorizontalSeparator(1,0,6)
	
	app.setStretch('both')
	app.setSticky('nesw')
	app.startFrame('frame_main')
	
	app.setSticky('nesw')
	app.setStretch('column')
	app.startLabelFrame('frame_main_entries',label='Entries')
	
	app.setSticky('nsw')
	app.setStretch('column')

	app.addLabel('label_Name',' Name:',1)
	app.addEntry('entry_Name',1,1)
	app.addLabel('label_Comment',' Comment:',6)
	app.addEntry('entry_Comment',6,1)
	app.addLabel('label_Keywords',' Keywords:',8)
	app.addEntry('entry_Keywords',8,1)
	app.addLabel('label_Exec',' Executable: ',10,0)
	app.addFileEntry('entry_Exec',10,1)
	app.addLabel('label_Icon',' Icon:',15,0)
	app.addFileEntry('entry_Icon',15,1)
	app.stopLabelFrame()

	app.startLabelFrame('frame_main_options',label='Options')
	app.setSticky('nesw')
	app.setStretch('column')
	app.addNamedCheckBox('Terminal','box_Terminal')
	app.addNamedCheckBox('NoDisplay','box_NoDisplay')
	app.addNamedCheckBox('PrefersNonDefaultGPU','box_PrefersNonDefaultGPU')
	app.addLabel('label_custom','Custom dict:',18,0)
	app.addEntry('entry_custom',18,1)
	app.addTickOptionBox('NotShowIn',[''],20,0)
	app.addTickOptionBox('OnlyShowIn',[''],20,1)
	app.stopLabelFrame()

	categories = {'AudioVideo':False,'Audio':False,'Video':False,'Development':False,'Education':False,'Game':False,'Graphics':False,'Network':False,'Office':False,'Science':False,'Settings':False,'System':False,'Utility':False}
	app.addProperties('Categories',categories,0,3,1,40)
	app.stopFrame()

	app.setStretch('column')
	app.setSticky('esw')
	app.startFrame('frame_bot')
	app.setStretch('both')
	app.startFrame('frame_bot_path',0,0)
	app.addLabelEntry('Path:',0,1,2)
	app.stopFrame()
	app.setStretch('none')
	app.startFrame('frame_bot_buttons',0,1)
	app.addButton('Save',iobuttons,0,3)
	app.setEntry('Path:','/usr/share/applications/unknown.dekstop',callFunction=False)
	app.stopFrame()
	app.stopFrame()



def update_default_filename():
	if filename_untouched:
		name = sanitize_filename(app.getEntry('entry_Name'))
		#stackoverflow.com/questions/8122079/python-how-to-check-a-string-for-substrings-from-a-list
		base_chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

		if any(substring in name for substring in base_chars) == False:
			name = 'unknown'
		app.setEntry('Path:',f'/usr/share/applications/{name}.desktop',callFunction=False)

def strip_ending_chars(string,char):
	loop = True
	while loop == True:
		if string.endswith(char):
			string = string[:-1]
		else:
			loop = False
	return string

def dict_specific_key(dictionary,key):
	key_list = []
	for entry in dictionary:
		if dictionary[entry] == key:
			key_list.append(entry)
	return key_list

def sanitize_filename(string):
	sanitizations = {' ':'_','/':'-',"'":'','"':'','`':'','\n':'','\\':'-'}
	for key in sanitizations:
		string = string.replace(key, sanitizations[key])
	string = strip_ending_chars(string,'.')
	return string

def audiovideo_check():
	if app.getProperty('Categories','Audio') or app.getProperty('Categories','Video'):
		if app.getProperty('Categories','AudioVideo') == False:
			app.setProperty('Categories','AudioVideo',value=True,callFunction=False)


def categories_updated():
	audiovideo_check()
	new_categories = dict_specific_key(app.getProperties('Categories'),True)
	if new_categories == []:
		new_categories = ['']
	app.changeOptionBox('NotShowIn',new_categories,callFunction=False)
	app.changeOptionBox('OnlyShowIn',new_categories,callFunction=True)

def optionbox_updated():
	onlyShow = dict_specific_key(app.getOptionBox('OnlyShowIn'),True)
	notShow = dict_specific_key(app.getOptionBox('NotShowIn'),True)
	if len(onlyShow) == 0 and len(notShow) > 0:
		app.disableOptionBox('OnlyShowIn')
	elif len(notShow) == 0 and len(onlyShow) > 0:
		app.disableOptionBox('NotShowIn')
	else:
		app.enableOptionBox('NotShowIn')
		app.enableOptionBox('OnlyShowIn')

def touch_filename():
	global filename_untouched
	if len(app.getEntry('Path:')) != ' ':
		filename_untouched = False
	else:
		filename_untouched = True
		update_default_filename()



def collect_entries():
	entries = {}
	entries_list = ['entry_Comment','entry_Name','entry_Icon','entry_Exec','entry_Keywords']
	for item in entries_list:
		item_value = app.getEntry(item)
		if item_value != '':
			item = item.replace('entry_','')
			entries[item] = item_value
	try:
		if not entries['Keywords'].endswith(';'):
			entries['Keywords'] = f'{entries["Keywords"]};'
	except:
		pass
	return entries

def collect_options():
	options = {}
	options_list = ['box_Terminal','box_NoDisplay','box_PrefersNonDefaultGPU']
	for item in options_list:
		item_value = app.getCheckBox(item)
		item = item.replace('box_','')
		options[item] = str(item_value).lower()
	NotShowIn = dict_specific_key(app.getOptionBox('NotShowIn'),True)
	OnlyShowIn = dict_specific_key(app.getOptionBox('OnlyShowIn'),True)
	if len(NotShowIn) > 0:
		options['NotShowIn'] = f'{";".join(NotShowIn)};'
	elif len(OnlyShowIn) > 0:
		options['OnlyShowIn'] = f'{";".join(OnlyShowIn)};'
	return options

def collect_categories():
	categories_list = dict_specific_key(app.getProperties('Categories'),True)
	if len(categories_list) >0:
		categories = {'Categories':f'{";".join(categories_list)};'}
	else:
		categories = {}
	return categories


def collect_all():
	base = {'Type':'Application','Version':'1.1'}
	entries = collect_entries()
	options = collect_options()
	categories = collect_categories()
	result = {**base, **entries, **options, **categories}
	if len(app.getEntry('entry_custom')) > 5:
		custom_dict = literal_eval(app.getEntry('entry_custom'))
		result = {**result, **custom_dict}
	return result

def iobuttons(name):
	if name == 'Save':
		if app.getEntry('entry_Name') != '':
			if app.getEntry('entry_Exec') == '':
				if app.questionBox('Missing entry','The executable field is empty. Continue?') == False:
					return
			fulldict = collect_all()
			print(fulldict)
			try:
				path = app.getEntry('Path:')
				config = configparser.ConfigParser()
				config.optionxform=str
				config['Desktop Entry'] = fulldict
				with open(path,'w') as file:
					config.write(file)
				app.infoBox('Success',f'File {path} successfully written.')
			except PermissionError:
				app.warningBox('Error',f'Insufficient permissions to write {path}.\nTry running as Root.')
		else:
			app.warningBox('Missing entry','The name field is required.')

def loops_n_events():
	app.setEntryChangeFunction('entry_Name',update_default_filename)
	app.setPropertiesChangeFunction('Categories',categories_updated)
	app.registerEvent(optionbox_updated)
	app.setEntryChangeFunction('Path:',touch_filename)
	app.setPollTime(250)

if __name__ == '__main__':
	filename_untouched = True
	app = gui('.desktop creator','600x430')
	app.setBg('ivory2',tint=True)
	app.setLabelFont(family='Open Sans')
	app.setFont(family='Open Sans')
	ui(app)

	loops_n_events()
	app.go()
