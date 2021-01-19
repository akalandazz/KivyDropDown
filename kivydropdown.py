from kivy.app import App 
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import NumericProperty,ObjectProperty, ListProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior, TouchRippleButtonBehavior
from kivy.uix.label import Label
KV = """
FloatLayout:
	CustomButton
		text:'Click Me'
		size_hint: None, None
        size: 100, 38
        pos_hint: {'center': (.5, .5)}
        items:["Action1", "Action2","Action3"]
        canvas.before:
        	Triangle:
        		points:self.x+(self.width/1.15), self.y+ self.height/1.6, \
        		self.x+(self.width/1.08), self.y+ self.height/2.5, \
        		self.x+self.width, self.y+ self.height/1.6
"""


class CustomDropdownChild(TouchRippleButtonBehavior, Label):
	pass



class CustomDropdown(DropDown):
    item_delay = NumericProperty(.1)
    display_time = NumericProperty(.5)
    def _start_animation(self):
        for i, w in enumerate(self.children[0].children): #w <<<< child buttons
            anim = (
                Animation(duration=i * self.item_delay)
                + Animation(opacity=1, duration=self.display_time)
            )
            w.opacity = 0
            anim.start(w)

        bar_color = self.bar_color

        def restore_bar_color(*args):
            Animation(bar_color=bar_color, d=self.display_time).start(self)

        self.bar_color = (0, 0, 0, 0)

        anim.bind(on_complete=restore_bar_color)

    def open_dropdown(self, widget):
        super(CustomDropdown, self).open(widget)
        self._start_animation()





class CustomButton(TouchRippleButtonBehavior, Label):
	drop = ObjectProperty()
	items = ListProperty()
	def __init__(self, **kwargs):
		super(CustomButton, self).__init__(**kwargs)
		fbind = self.fbind
		fbind('items', self._initiate_dropdown)


	def _initiate_dropdown(self, *args):
		self.drop = CustomDropdown()
		for item in self.items:
			self.drop.add_widget(CustomDropdownChild(text=item, size_hint_y=None, height=44, on_release = self._select))

		if not self.items:
			pass
		else:
			self.bind(on_release = self.drop.open_dropdown)

	def _select(self, wid):
		self.drop.dismiss()
		print(wid.text)

class MyApp(App):
	def build(self):
		return Builder.load_string(KV)


MyApp().run()