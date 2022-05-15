from tkinter import *
from tkinter import filedialog
from typing import Any


# from src.application.defaults import DEFAULT_DPI


class WidgetCustom:
    """Form widget base class to set default functions and values for all
    relevant widgets in the application."""

    default_font = ('Arial', 18)
    btn_pressed = False

    def __init__(self, widget_type, text_var=None, int_var=None, **kwargs):
        self.d_font = WidgetCustom.default_font
        self.displayable = True
        self.widget = None
        self.widget_type = widget_type
        self.text = text_var
        self.var = int_var
        self.kwargs = kwargs
        self.x_val = 0
        self.y_val = 0
        self.sup = self

    def place_custom(self, x_val: float = 0., y_val: float = 0.):

        """Method to make placing widgets on the screen easier.

        Parameters:
            x_val: rel-x position on window
            y_val: rel-y position on window"""

        # Updates x and y values
        self.x_val = x_val
        self.y_val = y_val
        try:
            self.widget.place(relx=x_val, rely=y_val, anchor=CENTER)
        except AttributeError:
            self.place(x_val, y_val, CENTER)
        finally:
            pass

    def get_value(self):

        """Method to return the widget's text value."""

        try:
            return self.widget.get()
        except AttributeError:
            if type(self.widget) is Checkbutton:
                return self.var.get()
            return self.text.get()
        finally:
            pass

    def set_value(self, value):
        """Method to set a label's text value."""
        try:
            self.text.set(value)
            print('---s')
        except AttributeError:
            print('---f')
            pass

    def toggle_widget(self, desired_state=0):

        """Method to make toggling the widget's appearance easier."""

        if self.displayable and desired_state == 0:
            print(self.__str__(), 'Toggled off')
            self.widget.place_forget()
            # if type(self) == FormInput:
            #     self.border.place_forget()
        elif not self.displayable and desired_state == 1:
            print(self.__str__(), 'Toggled on')
            self.place_custom(self.x_val, self.y_val)
        else:
            print('Nothing happened to', self.__str__())
            return
        self.displayable = not self.displayable

    def place(self, *args):
        print(self, "'s ", *args, " unused.", sep='')
        return None

    def initialize(self, widget_type, window, **kwargs):
        self.widget = widget_type(window, kwargs)

        if type(self.widget) == Label:
            self.text = StringVar(window, value=kwargs['text'])
            self.widget.configure(textvariable=self.text)
        if type(self.widget) == Checkbutton:
            self.var=IntVar()
            self.widget.configure(variable=self.var)
            # self.widget.config(width=15)


class LabelCustom(WidgetCustom):
    """Form label subclass of form widget.

    Creates a default Label widget based on settings for the form."""

    def __init__(self,
                 content='',
                 font_style=WidgetCustom.default_font,
                 width=25,
                 height=1,
                 border=2,
                 fg_color="white",
                 bg_color="black"):
        self.text = None
        # self.widget = Label(window,
        #                     text=content,
        #                     font=d_font_style,
        #                     width=d_width,
        #                     height=d_height,
        #                     bd=d_border,
        #                     fg=d_fg_color,
        #                     bg=d_bg_color,
        #                     textvariable=self.text)
        kwargs = dict(text=content,
                      font=font_style,
                      width=width,
                      height=height,
                      bd=border,
                      fg=fg_color,
                      bg=bg_color,
                      textvariable=self.text)
        # self.text.set(content)
        super().__init__(Label, **kwargs)


class InputCustom(WidgetCustom):
    """Form input subclass of form widget.

    Creates a default Entry widget based on settings for the form."""

    def __init__(self,
                 d_font_style=WidgetCustom.default_font,
                 d_width=15,
                 d_fg_color="white",
                 d_bg_color="black"):
        # self.border = Frame(window,
        #                     background="white",
        #                     width=d_width * DEFAULT_DPI / 6.85,
        #                     height=2.5 * DEFAULT_DPI / 6.85, )
        kwargs = dict(font=d_font_style,
                      width=d_width,
                      fg=d_fg_color,
                      bg='white',
                      bd=0)

        super().__init__(Entry, **kwargs)


class ButtonCustom(WidgetCustom):
    """Form reset button subclass of form widget.

    Creates a Button widget based on settings for the form. Configured to run
    a command to reset the application when clicked."""

    def __init__(self, cmd, content='', w=5, d_font_style=WidgetCustom.default_font):
        kwargs = dict(text=content,
                      width=w,
                      height=1,
                      font=d_font_style,
                      fg="black",
                      bg="white",
                      bd=0,
                      command=cmd)
        super().__init__(Button, **kwargs)

    # def attempt_reset(self):
    #     if FormWidget.btn_pressed:
    #         return
    #     FormWidget.btn_pressed = True
    #     reset()
    #     FormWidget.btn_pressed = False


class CheckbuttonCustom(WidgetCustom):

    def __init__(self, content=''):
        kwargs = dict(text=content,
                      font=super().default_font,
                      fg="black",
                      bg="white",
                      bd=0,
                      onvalue=1,
                      offvalue=0)
        super().__init__(Checkbutton, **kwargs)


class FileButtonCustom(WidgetCustom):
    """Form file button subclass of form widget.

    Creates a Button widget based on settings for the form. Configured to open
    a file dialog input system when clicked."""
    file_type: str

    def __init__(self, validated_cmd, invalidated_cmd=None, data_type='txt'):
        kwargs = dict(text="Browse File System",
                      font=super().default_font,
                      fg="black",
                      bg="white",
                      bd=0,
                      command=self._browse_files)
        self.validated_cmd = validated_cmd
        self.invalidated_cmd = invalidated_cmd
        self.file_type = data_type
        self.file_name = ''
        super().__init__(Button, **kwargs)

    def _browse_files(self):

        """Internal method to manage the filedialog window and resultantly
        attain the file path."""

        temp_name = filedialog.askopenfilename(title="Select a File",
                                               filetypes=(("File", str("." + self.file_type)),
                                                          ("all files", "*.*")))
        if self.file_name != '' and temp_name == '':
            return
        self.file_name = temp_name
        print(self.file_name)
        if self.file_name[-len(self.file_type):] == self.file_type:
            self.widget.configure(text='File inputted.')
            self.validated_cmd(self.file_name)
        else:
            self.invalidated_cmd()

    def get_file_lines(self):

        """Method to retrieve file lines separated as list items."""

        if self.file_name == '':
            return ['']
        file = open(self.file_name, "r", encoding="utf-8", errors="replace")
        lines = file.read().splitlines()
        file.close()
        return lines


class ScreenCustom:
    widgets: dict[str, WidgetCustom]

    def __init__(self, screen_manager, **kwargs):
        assert isinstance(screen_manager, ScreenManager)
        self.screen_manager = screen_manager
        self.widgets = {}
        for kwarg in kwargs:
            kwval = kwargs[kwarg]
            print("KWA:", kwarg, "| KWV:", kwval)
            self.widgets[kwarg] = kwval[0]
            print(self.widgets[kwarg])
            self.widgets[kwarg].initialize(self.widgets[kwarg].widget_type,
                                           self.screen_manager.window,
                                           **self.widgets[kwarg].kwargs)
            self.widgets[kwarg].place_custom(kwval[1], kwval[2])
            self.widgets[kwarg].toggle_widget(0)

    def set_screen(self):
        if self.screen_manager.current_screen is not Ellipsis:
            print(self.screen_manager.current_screen)
            for widget in self.screen_manager.current_screen.widgets:
                self.screen_manager.current_screen.widgets[widget].toggle_widget(0)
        for widget in self.widgets:
            self.widgets[widget].toggle_widget(1)
        self.screen_manager.current_screen = self

    # def initialize_screen(self, window):
    #     for n, widget in enumerate(self.widgets):
    #         self.widgets[n].initialize(widget, window, )
    #         self.widgets[n].toggle_widget()


class ScreenManager:
    current_screen: ScreenCustom
    screens: dict[str, Any]

    def __init__(self, window):
        self.screens = {}
        self.current_screen = ...
        self.window = window

    def __call__(self, *args, **kwargs):
        return self.get_screen(args[0])

    def get_screen(self, name: str = '', index: int = 0):
        screen: ScreenCustom = self.screens[list(self.screens)[index]] if name == '' else self.screens[name]
        return screen

    def add_screen(self, name, kwargs: dict[str, list[WidgetCustom, float, float]]) -> None:
        self.screens[name] = ScreenCustom(self, **kwargs)
