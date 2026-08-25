import flet as ft
import sqlite3

# Database တည်ဆောက်ခြင်း
def init_db():
    conn = sqlite3.connect("inventory.db", check_same_thread=False)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def main(page: ft.Page):
    page.title = "Offline Item Manager"
    page.window_width = 500
    page.window_height = 700
    
    # မြင်ကွင်းရှင်းလင်းစေရန် အဖြူရောင်နောက်ခံ (Light Mode)
    page.theme_mode = ft.ThemeMode.LIGHT 
    page.scroll = ft.ScrollMode.AUTO
    
    conn = init_db()

    # (၁) Data ထည့်ရန် UI
    name_input = ft.TextField(
        label="Item Name", 
        hint_text="ဥပမာ - USB Drive, ဇာတ်ကား", 
        width=200, 
        border_color="blue" 
    )
    price_input = ft.TextField(
        label="Price", 
        hint_text="ဥပမာ - 1500", 
        width=150, 
        border_color="blue"
    )
    
    # (၂) Search Box
    search_input = ft.TextField(
        label="Search by Name",
        hint_text="ရှာလိုသော ပစ္စည်းအမည် ရိုက်ထည့်ပါ",
        icon="search", 
        border_color="green",
        width=360,
        on_change=lambda e: load_data(e.control.value)
    )

    # (၃) ဇယား (Table) ပုံစံအစစ် ဖန်တီးခြင်း
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Item Name", color="blue", weight="bold")),
            ft.DataColumn(ft.Text("Price", color="blue", weight="bold")),
        ],
        rows=[]
    )

    # Data ရှာရန်နှင့် ပြသရန် Function
    def load_data(search_query=""):
        data_table.rows.clear() # ဇယားထဲက အဟောင်းတွေအရင်ဖျက်မယ်
        
        query = search_query if search_query else ""
        cursor = conn.execute("SELECT name, price FROM items WHERE name LIKE ?", ('%' + query + '%',))
        
        for row in cursor.fetchall():
            # Data တွေကို ဇယားအကွက် (Cell) တွေထဲ ထည့်ပါမယ်
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row[0])),
                        ft.DataCell(ft.Text(f"{row[1]} MMK")),
                    ]
                )
            )
        page.update()

    # Data အသစ်ထည့်ရန် Function
    def add_item(e):
        if name_input.value and price_input.value:
            conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name_input.value, price_input.value))
            conn.commit()
            
            name_input.value = ""
            price_input.value = ""
            name_input.update()
            price_input.update()
            
            current_search = search_input.value if search_input.value else ""
            load_data(current_search)

    # Screen ပေါ် နေရာချထားခြင်း
    page.add(
        ft.Text("Data ထည့်ရန်", size=18, weight="bold", color="blue"),
        ft.Row([name_input, price_input]),
        ft.ElevatedButton("Add Data", on_click=add_item, icon="add", bgcolor="blue", color="white"),
        
        ft.Divider(height=20, color="grey"),
        
        ft.Text("Data ရှာရန်", size=18, weight="bold", color="green"),
        search_input, 
        
        # ဇယားကို ဒီနေရာမှာ ထည့်ပါမယ်
        data_table 
    )
    
    load_data()

# App ကို Run မည်
ft.run(main)