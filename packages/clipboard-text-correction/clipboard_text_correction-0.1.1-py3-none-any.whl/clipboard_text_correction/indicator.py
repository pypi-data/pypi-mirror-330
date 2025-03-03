#!/usr/bin/python

import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7') 
from gi.repository import Gtk, AppIndicator3, Notify
from PyQt5.QtWidgets import QApplication

import clipboard_text_correction.lib_funcs as lib_funcs
import clipboard_text_correction.lib_files as lib_files
import clipboard_text_correction.lib_play  as lib_play
import clipboard_text_correction.lib_stats as lib_stats

import sys
import os
import json
import traceback

CONFIG_FILE = "~/.config/clipboard_text_correction/config_data.json"

config_data=lib_funcs.SYSTEM_DATA
config_file_path = os.path.expanduser(CONFIG_FILE)

try:
    if not os.path.exists(config_file_path):
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        
        with open(config_file_path, "w", encoding="utf-8") as arquivo:
            json.dump(config_data, arquivo, indent=4)
        print(f"Arquivo criado em: {config_file_path}")
        
    with open(config_file_path, "r") as arquivo:
        config_data = json.load(arquivo)
    
except FileNotFoundError:
    print(f"Erro: O arquivo '{config_file_path}' não foi encontrado.")
    sys.exit()
    
except json.JSONDecodeError:
    print(f"Erro: O arquivo '{config_file_path}' não contém um JSON válido.")
    sys.exit()


################################################################################
################################################################################
################################################################################

def show_notification_message(title,message,icon="emblem-generic"):
    Notify.init("ClipboardTextCorrection")
    notification = Notify.Notification.new(
        "⚠️ "+title+" ⚠️",
        message,
        icon
    )
    notification.show()
    
def show_message(message,width=600,height=300):
    """Exibe uma janela com uma mensagem copiável e um botão OK."""
    # Cria uma janela
    window = Gtk.Window(title="Message")
    window.set_default_size(width, height)

    # Cria o contêiner (Gtk.Box) para empacotar o conteúdo
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    box.set_border_width(10)

    # Cria o TextView para exibir a mensagem
    text_view = Gtk.TextView()
    text_buffer = text_view.get_buffer()
    text_buffer.set_text(message)  # Define o texto no TextBuffer
    text_view.set_wrap_mode(Gtk.WrapMode.WORD)  # Ativa a quebra de linha automática
    text_view.set_editable(False)  # Torna o TextView somente leitura
    text_view.set_cursor_visible(False)  # Oculta o cursor

    # Adiciona o TextView dentro de um ScrolledWindow para permitir rolagem
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.add(text_view)  # Adiciona o TextView ao ScrolledWindow
    box.pack_start(scrolled_window, True, True, 0)

    # Botão OK
    ok_button = Gtk.Button(label="OK")
    ok_button.connect("clicked", lambda x: window.close())
    box.pack_start(ok_button, False, False, 0)

    # Adiciona o contêiner à janela
    window.add(box)

    # Exibe a janela
    window.show_all()

    # Aguarda a janela ser fechada
    window.connect("destroy", Gtk.main_quit)
    Gtk.main()

def show_error_dialog(message):
    """Exibe um quadro de diálogo modal com a mensagem de erro usando Gtk, permitindo rolagem e cópia."""
    dialog = Gtk.Dialog(
        title="Error message",
        parent=None,
        modal=True,  # Substitui flags=Gtk.DialogFlags.MODAL
        destroy_with_parent=True
    )
    dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)

    # Caixa principal
    box = dialog.get_content_area()

    # Label para título do erro
    label = Gtk.Label(label="An error occurred:")
    label.set_halign(Gtk.Align.START)
    box.pack_start(label, False, False, 5)

    # Área de rolagem para o texto do erro
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    scrolled_window.set_size_request(400, 200)  # Define um tamanho mínimo

    # Campo de texto para exibir a mensagem de erro
    text_view = Gtk.TextView()
    text_view.set_editable(False)
    text_view.set_cursor_visible(False)
    text_view.set_wrap_mode(Gtk.WrapMode.WORD)

    # Inserir o erro no campo de texto
    buffer = text_view.get_buffer()
    buffer.set_text(message)

    # Adicionar campo de texto na rolagem
    scrolled_window.add(text_view)
    box.pack_start(scrolled_window, True, True, 5)

    # Mostrar todos os widgets
    dialog.show_all()

    # Esperar resposta do usuário
    dialog.run()
    dialog.destroy()


def select_file(initial_path=None):
    '''
    Return None se nao acha
    '''
    dialog = Gtk.FileChooserDialog(
        title="Select a file",
        action=Gtk.FileChooserAction.OPEN
    )

    if initial_path:
        dialog.set_current_folder(initial_path)

    # Adicionando botões usando o método add_buttons
    dialog.add_buttons(
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK
    )

    response = dialog.run()
    filename = dialog.get_filename() if response == Gtk.ResponseType.OK else None
    dialog.close()#dialog.destroy()
    
    while Gtk.events_pending():
        Gtk.main_iteration()
    
    return filename

def get_clipboard_text():
    # Verifica se QApplication já existe
    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Inicializa QApplication se não existir
    
    clipboard = app.clipboard()  # Acessa o clipboard
    text = clipboard.text()  # Obtém o texto do clipboard
    return text
    
def quit(source):
    Gtk.main_quit();



def basic_consult(type_consult, msg=None):
    if msg is None: 
        msg=get_clipboard_text()
    
    try:
        fmts=lib_files.detect_formats(msg)
        fmt=max(fmts, key=fmts.get)
        ext = lib_files.EXTENSION[fmt]
        
        
        texts = lib_files.split_text(msg, max_size=8000, separators=["\n\n", " ", ".", ","])
        
        all_out=""
        is_ok=True
        
        for index, text in enumerate(texts):
            show_notification_message(type_consult,f"{index+1}/{len(texts)} - The text was sent, please wait.")
            
            print(f"{index+1}/{len(texts)} - sent format:",fmt)
            
            res, OUT=lib_funcs.consultation_in_depth(config_data,
                                            lib_funcs.SYSTEM_QUESTION[type_consult]+
                                            f"\n- The text sent is probably written in {fmt} format.",
                                            text)
            
            if   res=="<OK>":
                all_out = all_out + OUT
            elif res=="<NOERROR>":
                all_out = all_out + text
            else:
                is_ok=False
                
            show_notification_message(type_consult,f"{index+1}/{len(texts)} - Answer {res} recived! "+lib_funcs.SYSTEM_RESPONSE[res])
            
            print("recived:", res)
            
            
        if is_ok:
            lib_files.compare_texts(msg,all_out,program='meld',filetype=ext)
        else:
            show_message("Errors in the query some answers were <ZERO>")


        
    except Exception as e:
        # Captura qualquer exceção e exibe o erro
        error_message = f"Error: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
        show_error_dialog(error_message)

def question_answer_consult(type_consult, msg=None):
    if msg is None: 
        msg=get_clipboard_text()
       
    try:
        fmts=lib_files.detect_formats(msg)
        fmt=max(fmts, key=fmts.get)
        ext = lib_files.EXTENSION[fmt]
        print("format:",fmt)
    
        show_notification_message(type_consult,"The text was sent, please wait.")
        
        res=lib_funcs.question_answer_in_depth( config_data,
                                                lib_funcs.SYSTEM_QUESTION[type_consult]+
                                                f"\n- The text sent is probably written in {fmt} format.",
                                                msg)
        show_message(res)
        
        
    except Exception as e:
        # Captura qualquer exceção e exibe o erro
        error_message = f"Error: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
        show_error_dialog(error_message)
################################################################################
        
def improve_writing(source):
    basic_consult("improve_writing")

def improve_scientific_writing(source):
    basic_consult("improve_scientific_writing")

def concise_writing(source):
    basic_consult("concise_writing")

def paraphrase(source):
    basic_consult("paraphrase")

################################################################################
def improves_file_writing(source):
    file_path=select_file()
    show_notification_message("Selected",file_path)

    if file_path:
        msg=lib_files.load_file_content(file_path)
        basic_consult("improve_writing", msg=msg)

################################################################################

def summarize_text(source):
    question_answer_consult("summarize_text")
    
def abstract_to_title(source):
    question_answer_consult("abstract_to_title")
    
def text_to_computer_science_abstract(source):
    question_answer_consult("text_to_computer_science_abstract")

################################################################################

def text_to_latex_equation(source):
    question_answer_consult("text_to_latex_equation")
    
def text_to_latex_table(source):
    question_answer_consult("text_to_latex_table")
    
################################################################################    
def statistics(source):
    msg=get_clipboard_text()
    res=lib_stats.generate_word_token_json(msg)
    show_message(res)
    
################################################################################

def edit_config(source):
    lib_files.open_from_filepath(config_file_path)
    
def open_url_usage(source):
    show_notification_message("open_url_usage",config_data["usage"])
    lib_files.open_url(config_data["usage"])
    
def open_url_help(source):
    url="https://github.com/trucomanx/ClipboardTextCorrection/blob/main/doc/README.md"
    show_notification_message("open_url_help",url)
    lib_files.open_url(url)

################################################################################
def buy_me_a_coffee(source):
    show_notification_message("Buy me a coffee","https://ko-fi.com/trucomanx")
    lib_files.open_url("https://ko-fi.com/trucomanx")


################################################################################
################################################################################

def main():
    # Criação do indicador
    indicator = AppIndicator3.Indicator.new(
        "clipboard-text-correction-indicador",                       # ID do indicador
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'logo.png'), 
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )

    # Criação do menu
    menu = Gtk.Menu()


    # Improve writing
    item_improve_writing = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("accessories-text-editor", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Improve writing")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_improve_writing.add(box)
    item_improve_writing.connect("activate", improve_writing)
    menu.append(item_improve_writing)
    
    
    # Improve scientific writing
    item_improve_scientific_writing = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("accessories-text-editor", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Improve scientific writing")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_improve_scientific_writing.add(box)
    item_improve_scientific_writing.connect("activate", improve_scientific_writing)
    menu.append(item_improve_scientific_writing)
    
    
    # Concise writing
    item_concise_writing = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("accessories-text-editor", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Concise writing")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_concise_writing.add(box)
    item_concise_writing.connect("activate", concise_writing)
    menu.append(item_concise_writing)


    # Paraphrase
    item_paraphrase = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("accessories-text-editor", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Paraphrase")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_paraphrase.add(box)
    item_paraphrase.connect("activate", paraphrase)
    menu.append(item_paraphrase)
    

    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()


    # Improves file writing
    item_improves_file_writing = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("edit-find-replace", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Improves file writing")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_improves_file_writing.add(box)
    item_improves_file_writing.connect("activate", improves_file_writing)
    menu.append(item_improves_file_writing)
    
    
    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Summarize text
    item_summarize_text = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("document-edit", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Summarize text")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_summarize_text.add(box)
    item_summarize_text.connect("activate", summarize_text)
    menu.append(item_summarize_text)
        
    
    # Abstract to title
    item_abstract_to_title = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("document-edit", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Abstract to title")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_abstract_to_title.add(box)
    item_abstract_to_title.connect("activate", abstract_to_title)
    menu.append(item_abstract_to_title)
    
    # Text to computer science abstract
    item_text_to_computer_science_abstract = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("document-edit", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Text to computer science abstract")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_text_to_computer_science_abstract.add(box)
    item_text_to_computer_science_abstract.connect("activate", text_to_computer_science_abstract)
    menu.append(item_text_to_computer_science_abstract)
    
    
    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Text to latex equation
    item_text_to_latex_equation = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("font-x-generic", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Text to latex equation")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_text_to_latex_equation.add(box)
    item_text_to_latex_equation.connect("activate", text_to_latex_equation)
    menu.append(item_text_to_latex_equation)
    
    
    # Text to latex table
    item_text_to_latex_table = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("font-x-generic", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Text to latex table")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_text_to_latex_table.add(box)
    item_text_to_latex_table.connect("activate", text_to_latex_table)
    menu.append(item_text_to_latex_table)

    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Statistics
    item_statistics = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("document-page-setup", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Text statistics")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_statistics.add(box)
    item_statistics.connect("activate", statistics)
    menu.append(item_statistics)
    
    
    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Open configfile
    item_edit_config = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("applications-utilities", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Open config file")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_edit_config.add(box)
    item_edit_config.connect("activate", edit_config)
    menu.append(item_edit_config)
    
    
    # Open url usage
    item_open_url_usage = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("applications-internet", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Open url usage")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_open_url_usage.add(box)
    item_open_url_usage.connect("activate", open_url_usage)
    menu.append(item_open_url_usage)
    
    
    # Open url help
    item_open_url_help = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("help-contents", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Open url help")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_open_url_help.add(box)
    item_open_url_help.connect("activate", open_url_help)
    menu.append(item_open_url_help)
    
    
    
    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Buy me a coffee
    item_buy_me_a_coffee = Gtk.MenuItem()
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    icon = Gtk.Image.new_from_icon_name("emblem-favorite", Gtk.IconSize.MENU)  # Nome do ícone do sistema
    label = Gtk.Label(label="Buy me a coffee: TrucomanX")
    box.pack_start(icon, False, False, 0)
    box.pack_start(label, False, False, 0)
    item_buy_me_a_coffee.add(box)
    item_buy_me_a_coffee.connect("activate", buy_me_a_coffee)
    menu.append(item_buy_me_a_coffee)
    
    
    # Adicionando um separador
    separator = Gtk.SeparatorMenuItem()
    menu.append(separator)
    separator.show()
    
    
    # Adicionando exit
    item_quit = Gtk.MenuItem(label="Exit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)

    # Mostrar o menu
    menu.show_all()

    # Associar o menu ao indicador
    indicator.set_menu(menu)

    # Exibir o indicador
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    # Manter o aplicativo rodando
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()

if __name__ == '__main__':
    main();
