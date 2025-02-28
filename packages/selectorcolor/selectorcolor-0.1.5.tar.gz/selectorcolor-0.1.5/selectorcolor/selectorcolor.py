import flet as ft
from time import sleep

class SelectorColor(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = True

        self.slides = {
            l: ft.Slider(
                min=0, 
                max=255, 
                value=0,
                height=30, 
                width=320,                
                active_color="#00ADFF",
                thumb_color ="#00ADFF",
                on_change=self.update_color,                 
            ) 
            for l in ['r', 'g', 'b']
        }

 

        self.titulo = ft.Text(
            value="Título", 
            selectable=True,
            size = 20, 
            weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto1 = ft.Text(
            value="Texto 1", 
            selectable=True,
            size = 15, 
            # weight= 'BOLD', 
            color = '#ffffff'
        )
        self.texto2 = ft.Text(
            value="Texto 2", 
            selectable=True,
            size = 12, 
          
            color = '#ffffff'
        )                
        self.color_text = ft.Text(
            value="Texto", 
            selectable=True,
            size = 20, 
            weight= 'BOLD', 
            color = '#ffffff'
        )
        self.color_box = ft.Container(
            content = self.color_text, 
            width=100, 
            height=100, 
            bgcolor="#ff0000", 
            border_radius=12,
            alignment=ft.alignment.center,
           
        )
        self.color_box2 = ft.Container(
            content=ft.Column(
                controls = [
                    self.titulo,
                    self.color_box,
                    self.texto1,
                    self.texto2
                ],
                horizontal_alignment='center',
                tight=True,
                spacing= 3,
            ),
            alignment=ft.alignment.center,
            width=210, 
            height=210, 
            border_radius=12,
            bgcolor="#0000ff",

            )
        
        self.gradiente = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#000000", "#000000"],
        )
        self.sombras = ft.BoxShadow(spread_radius=0, blur_radius=20, color='black')        

        self.ativar_sombras = ft.Checkbox(label="Ativar Sombras", value =False, on_change=self.GerenciarSombras)
        self.ativar_gradiente = ft.Checkbox(label="Ativar Gradiente", value =False, on_change=self.GerenciarGradiente)
        self.ativar_bordas = ft.Checkbox(label="Ativar Bordas", value =False, on_change=self.GerenciarBordas)

        self.color_scheme=ft.ColorScheme()

        self.datas = {
            "Container": lambda color: setattr(self.color_box, 'bgcolor', color), 
            "Fundo": self.ChangeFundoColor,
            "Texto": lambda color: setattr(self.color_text, 'color', color),
            "Título": lambda color: setattr(self.titulo, 'color', color),
            "Texto 1": lambda color: setattr(self.texto1, 'color', color),
            "Texto 2": lambda color: setattr(self.texto2, 'color', color),
            "Bordas": self.ChangeBordasColor,
            "Sombras": self.ChangeSombrasColor,
            "Gradiente": self.ChangeGradienteColor, 
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
        }


        legenda = {
            'primary': 'primary: texto principal, fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone,  texto do elevatebuton',
            'on_primary': 'on_primary: texto filledbutton e bolinha do swicth com True',
            'on_secondary_container': 'on_secondary_container: texto filledtonalbutton',
            'outline': 'outline: borda do outliedbutton',
            'shadow': 'shadow: sombras',
            'on_surface_variant': 'on_surface_variant: labels, cor da caixa do checkbox e cor do check do popMenubutton',
            'surface_variant': 'surface_variant: slider e fundo do texfield e do dropbox',
            'primary_container': 'primary_container: HOVERED da bolinha do switch',
            'on_surface': 'on_surface: HOVERED do checkbox e cor dos items do popmenubuton',
            'surface': 'surface: cor de fundo',
  

        }
        # self.tabela_legenda = ft.DataTable(
        #     column_spacing = 10,
        #     data_row_max_height=80,
        #     columns=[ft.DataColumn(ft.Text(i, weight='BOLD')) for i in ['Cor', 'Descrição']],
        #     rows=[
        #         ft.DataRow(
        #             cells=[
        #                 ft.DataCell(
        #                     ft.Text(linha)
        #                 ),
        #                 ft.DataCell(
        #                     ft.Text(legenda[linha])
        #                 )
        #             ]
        #         ) 
        #         for linha in legenda.keys()
        #     ],
        #     border = ft.border.all(1, 'primary'),
        #     vertical_lines = ft.BorderSide(1, 'primary'),
        #     heading_row_color = 'grey800',
        # )

        self.tabela_legenda = ft.Column(
            controls = [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(i, weight='BOLD',width=160,text_align='center'),
                            ft.VerticalDivider(10, color='primary,0.5'),
                            ft.Text(legenda[i],width=220,)
                        ],
                        spacing=0,
                    ),
                    expand = True,
                    
                    border=ft.border.all(1, 'primary,0.5'),
                )
                for i in legenda.keys()
           
            ],
            spacing=0,
            run_spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            width=400,
            # expand=True,
        )

        self.objetos = ft.Dropdown(
            width=350,
            options=[ft.dropdown.Option(i) for i in self.datas.keys()],
            hint_text="Selecione o objeto",
            filled=True,
            border_radius=15,
            on_change=self.SetObjeto,
            enable_filter = True,
            enable_search = True,
            editable=True
            
        )

        self.cor = 'black'

        self.btn_exportar_cores = ft.ElevatedButton(
            text="Exportar",
            tooltip="Exportar as cores \npara área de transferência",
            on_click=self.ExportarCores,
        )
      
        self.content = ft.Row(
            controls = [                                                      
                self.color_box2,
                ft.Container(
                    content = ft.Column(
                        [
                            ft.Row([self.ativar_sombras, self.ativar_bordas, self.ativar_gradiente], alignment='center', spacing=1,wrap=False),
                            ft.Row(
                                    [
                                   self.objetos,
                                    ft.IconButton(
                                        icon=ft.Icons.COPY, 
                                        icon_size = 10,                                       
                                        splash_radius=0,
                                        on_click=lambda e: e.page.set_clipboard(f'"{self.cor}"')
                                    )
                                ], 
                                spacing = 0,
                                wrap=False,                                       
                            ),                                    
                            ft.Row([ft.Text("Vermelho", selectable=True, width=70),self.slides[f'r'],], spacing=0),
                            ft.Row([ft.Text("Verde", selectable=True, width=70),self.slides[f'g'],], spacing=0),
                            ft.Row([ft.Text("Azul", selectable=True, width=70),self.slides[f'b'],], spacing=0),
                        ],
                        width=380,
                        spacing=0,
                        run_spacing=0,
                        horizontal_alignment='center',
                    ),
                    border=ft.border.all(1, 'grey800'),
                    border_radius=15,
                    padding=20,
                ),
                ft.Row([self.btn_exportar_cores], alignment='center',),
                self.tabela_legenda,                                                           
            ], 
            wrap=True,
            spacing=20,
            run_spacing=10,
            alignment='center',
            vertical_alignment='center',
        )

    def ExportarCores(self, e):
        cores =f'''
cores = {{  
    "Container": {self.color_box.bgcolor},
        "Fundo": {self.color_box2.bgcolor},
        "Texto": {self.color_text.color},
        "Título": {self.titulo.color},
        "Texto 1": {self.texto1.color},
        "Texto 2": {self.texto2.color},
        "Bordas": {self.sombras.color},
        "Sombras": {self.sombras.color},
        "Gradiente": {self.gradiente.colors},
        "primary":  {self.color_scheme.primary},
        "on_primary":  {self.color_scheme.on_primary},
        "on_secondary_container":  {self.color_scheme.on_secondary_container},
        "outline":  {self.color_scheme.outline},
        "shadow":  {self.color_scheme.shadow},
        "on_surface_variant":  {self.color_scheme.on_surface_variant},
        "surface_variant":  {self.color_scheme.surface_variant},
        "primary_container":  {self.color_scheme.primary_container},
        "on_surface":  {self.color_scheme.on_surface},
        "surface":  {self.color_scheme.surface},
    }}'''
        self.page.set_clipboard(cores)

    def ChangeBordasColor(self, color):
        if self.ativar_bordas.value:
            self.bordas = ft.border.all(1, color)
            setattr(self.color_box, 'border', self.bordas)
            self.color_box.update()
            self.update()

    def ChangeSombrasColor(self, color):
        if self.ativar_sombras.value:
            self.sombras.color = color
            setattr(self.color_box, 'shadow', self.sombras)
            self.color_box.update()
            self.update()


    def ChangeGradienteColor(self, color):
        if self.ativar_gradiente.value:
            self.gradiente.colors[1] = color
            setattr(self.color_box2, 'gradient', self.gradiente)
            self.color_box2.update()
            self.update()

    def ChangeFundoColor(self, color):
        if not self.ativar_gradiente.value:
            setattr(self.color_box2, 'bgcolor', color)
        else:
            self.gradiente.colors[0] = color
            setattr(self.color_box2, 'gradient', self.gradiente)
        self.color_box2.update()
        self.update()

    def SetObjeto(self, e):
        self.slides['r'].data = e.control.value
        self.slides['g'].data = e.control.value
        self.slides['b'].data = e.control.value

    def GerenciarSombras(self, e):
        if self.ativar_sombras.value:
            self.color_box.shadow = self.sombras
        else:
            self.color_box.shadow = None
        # self.sombras.visible = self.ativar_sombras.value
        self.color_box.update()
        self.update()

    def GerenciarGradiente(self, e):
        if self.ativar_gradiente.value:
            # cor = self.GetColorSafe('Gradiente') or 'blue'
            self.color_box2.gradient = self.gradiente
        else:
            self.color_box2.gradient = None
        # self.gradiente.visible = self.ativar_gradiente.value
        self.color_box2.update()
        self.update()

    def GerenciarBordas(self, e):
        if self.ativar_bordas.value:
            self.color_box.border = self.bordas
        else:
            self.color_box.border = None
        # self.bordas.visible = self.ativar_bordas.value
        self.color_box.update()
        self.update()

    def update_color(self, e):
        if e.control.data:
            self.cor = f'#{int(self.slides['r'].value):02X}{int(self.slides['g'].value):02X}{int(self.slides['b'].value):02X}'
            self.datas[e.control.data](self.cor)
            self.update()
            self.page.update()
            self.SetValueCLienStorage(f'{self.page.title}_{e.control.data}', self.cor)


    def SetValueCLienStorage(self, key, value, retries=3, delay=1):
        for attempt in range(retries):
            try:
                self.page.client_storage.set(key, value)
                return
            except TimeoutError as e:
                if attempt < retries - 1:
                    print(f"Tentativa {attempt + 1} falhou. Tentando novamente após {delay} segundos...")
                    sleep(delay)
                else:
                    raise e

    def GetColorSafe(self, key):
        return self.page.client_storage.get(f'{self.page.title}_{key}')

    def did_mount(self):
        self.titulo.color = self.GetColorSafe('Título')
        self.texto1.color = self.GetColorSafe('Texto 1')
        self.texto2.color = self.GetColorSafe('Texto 2')         
        self.color_text.color = self.GetColorSafe('Texto')
        self.color_box.bgcolor = self.GetColorSafe('Container')
        self.color_box2.bgcolor = self.GetColorSafe('Fundo')
        self.gradiente.colors = [self.color_box2.bgcolor, self.GetColorSafe('Gradiente')]
        self.sombras.color = self.GetColorSafe('Sombras')
        self.bordas = ft.border.all(1, self.GetColorSafe('Bordas'))
    
        self.page.theme = ft.Theme(
            # color_scheme=self.color_scheme,
            primary_color  ='blue',
            
        )
        self.page.update()

class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_min = None, height_min = None, onlyresize = False):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_min = width_min
        self.height_min = height_min
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.onlyresize = onlyresize
        if not onlyresize:
            self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.nome = f'{self.page.title}_tamanho'
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    async def window_event(self, e):
        if e.data == 'resized' or e.data == 'moved':
            await self.page_resize(e)
        if e.data == "close" and not self.onlyresize:
            self.page.overlay.append(self.confirm_dialog)
            
            self.confirm_dialog.open = True
            self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()



    async def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]
        if self.height_min:
            if valores[1]< self.height_min:
                valores[1] = self.height_min
        if self.width_min:
            if valores[0]< self.width_min:
                valores[0] = self.width_min      
        if valores[2] <0:
              valores[2] = 0   
        if valores[3] <0:
              valores[3] = 0                
        # with open('assets/tamanho.txt', 'w') as arq:
        #     arq.write(f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        await self.page.client_storage.set_async(self.nome, f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        

  

    def Ler_dados(self):
        try:
            # with open('assets/tamanho.txt', 'r') as arq:
            #     po = arq.readline()

            po = self.page.client_storage.get(self.nome)

            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 

            if self.width_min:
                if po[0]< self.width_min:
                    po[0] = self.width_min  
            if self.height_min:
                if po[1]< self.height_min:
                    po[1] = self.height_min 
            if po[2] <0:
                po[2] = 0   
            if po[3] <0:
                po[3] = 0                                   

            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            # with open('assets/tamanho.txt', 'w') as arq:
            #     arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = self.width_min,self.height_min,0,0

def main(page):
    page.title = "Seletor de Cores"
    page.window.width = 700
    page.window.height = 300
    ConfirmarSaidaeResize(page = page, exibir=True, onlyresize=True)
    page.theme = ft.Theme(
        elevated_button_theme = ft.ElevatedButtonTheme(
            bgcolor   = None,
            icon_color  = None,
            shadow_color  = None,
            text_style = ft.TextStyle(color  = None),
        ),
        checkbox_theme = ft.CheckboxTheme(
            check_color = None,
            fill_color  = None,
        )
    )

    page.add(
        SelectorColor()
    )
def Iniciar():
    ft.app(target=main)
if __name__ == "__main__":  
    ft.app(target=main)
