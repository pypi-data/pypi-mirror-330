from sys import path as pthsys
# pthsys.append(r'D:\baixados\programas_python\baixar_do_youtube_final')

import flet as ft
from selectorcolor import SelectorColor

# from pathlib import Path

# Adicione o diretório raiz do projeto ao PATH do Python
# CAMINHO_RAIZ = Path(__file__).parent.parent  # Volta duas pastas (layout -> projeto)
class SelectorColor2(SelectorColor):
    def __init__(self, control, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.control = control
        self.width = None

        self.datas = {
            # "Container": lambda color: setattr(self.color_box, 'bgcolor', color), 
            "Fundo": self.ChangeFundoColor,
            "Texto": lambda color: setattr(self.text_theme, 'color', color),
            # "Título": lambda color: setattr(self.titulo, 'color', color),
            # "Texto 1": lambda color: setattr(self.texto1, 'color', color),
            # "Texto 2": lambda color: setattr(self.texto2, 'color', color),
            # "Bordas": self.ChangeBordasColor,
            # "Sombras": self.ChangeSombrasColor,
            "Gradiente": self.ChangeGradienteColor, 
            "Botão": self.ChangeBotao,
            "bgcolor":lambda color: setattr(self.control, 'bgcolor', color),
            "color":lambda color: setattr(self.control, 'color', color),
            # "dropdown_menu_theme":lambda color: setattr(self.page.theme.dropdown_menu_theme.text_style, 'bgcolor', color),
            "primary":  lambda color: setattr(self.color_scheme, 'primary', color),
            "on_primary":  lambda color: setattr(self.color_scheme, 'on_primary', color),
            "on_secondary_container":  lambda color: setattr(self.color_scheme, 'on_secondary_container', color),
            "outline":  lambda color: setattr(self.color_scheme, 'outline', color),
            "shadow":  lambda color: setattr(self.color_scheme, 'shadow', color),
            "on_surface_variant":  lambda color: setattr(self.color_scheme, 'on_surface_variant', color),
            "surface_variant":  lambda color: setattr(self.color_scheme, 'surface_variant', color),
            "primary_container":  lambda color: setattr(self.color_scheme, 'primary_container', color),
            "on_surface":  lambda color: setattr(self.color_scheme, 'on_surface', color),
            "surface":  lambda color: setattr(self.color_scheme, 'surface', color),




            "secondary": lambda color: setattr(self.color_scheme, 'secondary', color),
            "secondary_container": lambda color: setattr(self.color_scheme, 'secondary_container', color),
            "on_secondary_container": lambda color: setattr(self.color_scheme, 'on_secondary_container', color),
            "tertiary": lambda color: setattr(self.color_scheme, 'tertiary', color),
            "on_tertiary": lambda color: setattr(self.color_scheme, 'on_tertiary', color),
            "tertiary_container": lambda color: setattr(self.color_scheme, 'tertiary_container', color),
            "on_tertiary_container": lambda color: setattr(self.color_scheme, 'on_tertiary_container', color),
            "error": lambda color: setattr(self.color_scheme, 'error', color),
            "on_error": lambda color: setattr(self.color_scheme, 'on_error', color),
            "error_container": lambda color: setattr(self.color_scheme, 'error_container', color),
            "on_error_container": lambda color: setattr(self.color_scheme, 'on_error_container', color),
            "background": lambda color: setattr(self.color_scheme, 'background', color),
            "on_background": lambda color: setattr(self.color_scheme, 'on_background', color),
            "outline_variant": lambda color: setattr(self.color_scheme, 'outline_variant', color),
            "scrim": lambda color: setattr(self.color_scheme, 'scrim', color),
            "inverse_surface": lambda color: setattr(self.color_scheme, 'inverse_surface', color),
            "on_inverse_surface": lambda color: setattr(self.color_scheme, 'on_inverse_surface', color),
            "inverse_primary": lambda color: setattr(self.color_scheme, 'inverse_primary', color),
            "surface_tint": lambda color: setattr(self.color_scheme, 'surface_tint', color),
            "on_primary_fixed": lambda color: setattr(self.color_scheme, 'on_primary_fixed', color),
            "on_secondary_fixed": lambda color: setattr(self.color_scheme, 'on_secondary_fixed', color),
            "on_tertiary_fixed": lambda color: setattr(self.color_scheme, 'on_tertiary_fixed', color),
            "on_primary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_primary_fixed_variant', color),
            "on_secondary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_secondary_fixed_variant', color),
            "on_tertiary_fixed_variant": lambda color: setattr(self.color_scheme, 'on_tertiary_fixed_variant', color),
            "primary_fixed": lambda color: setattr(self.color_scheme, 'primary_fixed', color),
            "secondary_fixed": lambda color: setattr(self.color_scheme, 'secondary_fixed', color),
            "tertiary_fixed": lambda color: setattr(self.color_scheme, 'tertiary_fixed', color),
            "primary_fixed_dim": lambda color: setattr(self.color_scheme, 'primary_fixed_dim', color),
            "secondary_fixed_dim": lambda color: setattr(self.color_scheme, 'secondary_fixed_dim', color),
            "surface_bright": lambda color: setattr(self.color_scheme, 'surface_bright', color),
            "surface_container": lambda color: setattr(self.color_scheme, 'surface_container', color),
            "surface_container_high": lambda color: setattr(self.color_scheme, 'surface_container_high', color),
            "surface_container_low": lambda color: setattr(self.color_scheme, 'surface_container_low', color),
            "surface_container_lowest": lambda color: setattr(self.color_scheme, 'surface_container_lowest', color),
            "surface_dim": lambda color: setattr(self.color_scheme, 'surface_dim', color),
            "tertiary_fixed_dim": lambda color: setattr(self.color_scheme, 'tertiary_fixed_dim', color),
            
        }

        self.objetos.options=[ft.dropdown.Option(i) for i in self.datas.keys()]
        self.controles.col =  12
        self.color_box2.col =  12
        self.color_box2.expand =  True
        self.color_box2.height =  None
        self.color_box2.content = self.control
        self.controles.content.controls[0].controls[0].visible = False
        self.controles.content.controls[0].controls[1].visible = False
        self.content = ft.Column(
            controls = [
                ft.ResponsiveRow(
                    controls = [
                        self.caixa(self.color_box2, col = 8),
                        self.caixa(
                            ft.Column(
                                [
                                    self.controles,

                                    ft.ResponsiveRow(
                                        [self.btn_exportar_cores, self.tema_escolhido], 
                                        alignment='center', 
                                        vertical_alignment='center'                                                      
                                    ),
                                    ft.ResponsiveRow(
                                        [self.btn_save,self.nome_tema,]
                                        , alignment='center',                           
                                    ),
                                    
                                    self.tabela_legenda, 
                                    
                                ],
                                
                                scroll=ft.ScrollMode.ADAPTIVE,
                                expand=True,
                            ),
                            col = 4
                        )
                                          
                    ],
                    alignment='center', 
                    columns=12
                
                ),                                                                                                                            
            ], 
            # alignment='center',
            horizontal_alignment='center',
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,  
        )

    def ChangeBotao(self, color):
        self.botao.bgcolor = color
        self.page.theme.elevated_button_theme.bgcolor = color
        self.update()
        self.page.update()
        print('botão')
        # self.SetValueCLienStorage(f'{self.page.title}_Botao', color)
        # self.dic['Botao'] = self.cor

    def caixa(self, control, col = 12):
        return ft.Container(
            padding=15,
            border=ft.border.all(1, 'grey800'),
            border_radius=15,
            col = col,
            content=control,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=60,
                color='#524A76,0.2',
                blur_style = ft.ShadowBlurStyle.OUTER
            )
        )
    def update_color(self, e):
        if e.control.data:
            self.cor = f'#{int(self.slides['r'].value):02X}{int(self.slides['g'].value):02X}{int(self.slides['b'].value):02X}'
            self.datas[e.control.data](self.cor)
            self.update()
            self.page.update()
            # self.SetValueCLienStorage(f'{self.page.title}_{e.control.data}', self.cor)
            self.dic[e.control.data] = self.cor        

    def ExportarCores(self, e):

        cores =f'''

        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary = "{self.color_scheme.primary}",
                on_primary = "{self.color_scheme.on_primary}",
                on_secondary_container = "{self.color_scheme.on_secondary_container}",
                outline = "{self.color_scheme.outline}",
                shadow = "{self.color_scheme.shadow}",
                on_surface_variant = "{self.color_scheme.on_surface_variant}",
                surface_variant = "{self.color_scheme.surface_variant}",
                primary_container = "{self.color_scheme.primary_container}",
                on_surface = "{self.color_scheme.on_surface}",
                surface = "{self.color_scheme.surface}",
            ),
            text_theme = ft.TextTheme(
                body_medium=ft.TextStyle(color="{self.text_theme.color}")  # Cor do texto padrão
            )   
        ) 
        page.bgcolor =  'surface'   
    '''
        self.page.set_clipboard(cores)

def Iniciar(control):
    def main(page: ft.Page):
        page.title = 'Selector de Cores2'
        page.add(SelectorColor2(control))
    ft.app(target=main)


if __name__ == '__main__':
    Iniciar(ft.TextField(label='teste', value = 'askjdhaklsjhkj'))