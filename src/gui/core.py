import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from webcolors import hex_to_rgb
import gui.data


def run_gui(show_demo=False, config=None):
    if not config:
        print("GUI Configuration data not passed to GUI module")
        exit()

    dpg.create_context()

    dpg.create_viewport(title='Car Speaker Audio Degrader', width=int(config["WINDOW_SIZE_X"]), height=int(config["WINDOW_SIZE_Y"]))
    dpg.set_viewport_resizable(False)

    assemble_gui(config)

    if show_demo:
        demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.set_primary_window("windowMain", True)

    dpg.start_dearpygui()
    dpg.destroy_context()


def assemble_gui(config=None):
    '''with dpg.font_registry():
        regular_font = dpg.add_font("Graphics\\Fonts\\RobotoMono-SemiBold.ttf", config['UI_FONT_SIZE_REGULAR'])
        small_font = dpg.add_font("Graphics\\Fonts\\RobotoMono-SemiBold.ttf", config['UI_FONT_SIZE_SMALL'])
        large_font = dpg.add_font("Graphics\\Fonts\\RobotoMono-SemiBold.ttf", config['UI_FONT_SIZE_LARGE'])
        header_font = dpg.add_font("Graphics\\Fonts\\RobotoMono-Bold.ttf", config['UI_FONT_SIZE_HEADER'])
        title_font = dpg.add_font("Graphics\\Fonts\\RobotoMono-Bold.ttf", config['UI_FONT_SIZE_TITLE'])
        dpg.bind_font(regular_font)
        dpg.bind_font(small_font)
        dpg.bind_font(large_font)
        dpg.bind_font(header_font)
        dpg.bind_font(title_font)'''  # TODO: Crashes DPG, prevents font loading

    set_gui_colors(config)  # TODO: This doesn't actually set the colors
    set_gui_style(config)

    with dpg.window(tag="windowMain"):
        with dpg.tab_bar():
            for pagedata in gui.data.pagedata:
                with dpg.tab(label=pagedata["title"]):
                    with dpg.child_window():
                        if pagedata.get('header'):
                            header = dpg.add_text(pagedata.get('header'))
                            '''dpg.bind_item_font(header, header_font)'''

                        if pagedata.get('body') and pagedata.get('body') is str:
                            body = dpg.add_text(pagedata.get('body'))
                            '''dpg.bind_item_font(body, regular_font)'''
                        elif pagedata.get('body') and callable(pagedata.get('body')): # TODO: This should check for code, not allowing anything else
                            pagedata.get('body')()

                        if pagedata.get('footer'):
                            footer = dpg.add_text(pagedata.get('footer'))
                            '''dpg.bind_item_font(footer, small_font)'''


def set_gui_colors(config=None):  # Set up theme and colors
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, hex_to_rgb(config["BACK_COLOR"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, hex_to_rgb(config["BACK_COLOR_LIGHT"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, hex_to_rgb(config["ACCENT_COLOR"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, hex_to_rgb(config["ACCENT_COLOR_DARK"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, hex_to_rgb(config["ACCENT_COLOR"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hex_to_rgb(config["ACCENT_COLOR_DARK"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, hex_to_rgb(config["BACK_COLOR_LIGHT"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, hex_to_rgb(config["ACCENT_COLOR_DARK"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, hex_to_rgb(config["ACCENT_COLOR"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, hex_to_rgb(config["ACCENT_COLOR"]), category=dpg.mvThemeCat_Core)

    dpg.bind_theme(global_theme)


def set_gui_style(config=None):
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 5, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 12, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, int(config["UI_CORNER_RADIUS"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, int(config["UI_CORNER_RADIUS"]), category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, int(config["UI_SCROLLBAR_SIZE"]), category=dpg.mvThemeCat_Core)

    dpg.bind_theme(global_theme)
