import re

# 默认颜色字典
DEFAULT_COLORS = {
    'primary': '#3498db',    # 默认主色
    'secondary': '#2980b9',  # 默认次色/悬停颜色
    'background': '#f5f6f5', # 背景颜色
    'text': '#333333',       # 默认文本颜色
    'border': '#ddd',        # 边框和线条颜色
    'shadow': 'rgba(0, 0, 0, 0.2)'  # 阴影颜色
}

class HtmlGenerator:
    def __init__(self, page_dict):
        self.page_dict = page_dict
        self.colors = {**DEFAULT_COLORS, **page_dict.get('style', {}).get('colors', {})}
        self.layout = page_dict.get('layout', {'show_header': True, 'show_sidebar': True})

    # 生成内联样式的辅助函数
    def get_inline_style(self, prefix):
        primary_color = self.colors['primary']
        secondary_color = self.colors['secondary']
        background_color = self.colors['background']
        text_color = self.colors['text']
        border_color = self.colors['border']
        shadow_color = self.colors['shadow']
        
        # 大多数元素的基本样式
        style = f"""
        background-color: {background_color};
        color: {text_color};
        border: 1px solid {border_color};
        box-shadow: 0 4px 15px {shadow_color};
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        max-width: 800px;
        """
        
        # 根据前缀的特定样式
        if prefix.endswith('-btn'):
            style = f"""
            background-color: {primary_color};
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 2px 6px {shadow_color};
            transition: background-color 0.3s;
            """
        elif prefix.endswith('-table'):
            style = f"""
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            border: 1px solid {border_color};
            box-shadow: 0 4px 15px {shadow_color};
            """
        elif prefix.endswith('-list') or prefix.endswith('-menu'):
            style = f"""
            list-style: none;
            padding: 0;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px {shadow_color};
            padding: 15px;
            """
        elif prefix.endswith('-item'):
            style = f"""
            margin: 10px 0;
            """
        elif prefix.endswith('-th') or prefix.endswith('-td'):
            style = f"""
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid {border_color};
            """
        elif prefix.endswith('-form'):
            style = f"""
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 15px {shadow_color};
            padding: 15px;
            """
        elif prefix.endswith('-label'):
            style = f"""
            color: {text_color};
            """
        elif prefix.endswith('-input'):
            style = f"""
            padding: 5px;
            border: 1px solid {border_color};
            border-radius: 4px;
            """
        elif prefix.endswith('-p'):
            style = f"""
            color: {text_color};
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px {shadow_color};
            """
        elif prefix in ['header', 'sidebar', 'content']:
            if prefix == 'header':
                style = f"""
                background-color: {primary_color};
                color: white;
                padding: 10px;
                text-align: center;
                box-shadow: 0 2px 10px {shadow_color};
                """
            elif prefix == 'sidebar':
                style = f"""
                width: 200px;
                background-color: {background_color};
                padding: 10px;
                float: left;
                height: 100vh;
                border-right: 1px solid {border_color};
                box-shadow: 0 2px 10px {shadow_color};
                """
            elif prefix == 'content':
                style = f"""
                margin-left: 220px;
                padding: 20px;
                """
        return style.strip()

    # 生成侧边栏菜单
    def generate_sidebar(self, sidebar_items, prefix):
        if not prefix:
            raise ValueError("Prefix is required for sidebar")
        style = self.get_inline_style(prefix + '-menu')
        html = f'<ul id="{prefix}-menu" class="{prefix}-menu" style="{style}">\n'
        for item in sidebar_items:
            text = item.get('text', '').lower().replace(" ", "-")
            href = item.get('href', '#')
            item_style = self.get_inline_style(prefix + '-item')
            html += f'    <li id="{prefix}-item-{text}" class="{prefix}-item" style="{item_style}"><a href="{href}">{item["text"]}</a></li>\n'
        html += '</ul>\n'
        return html

    # 生成列表
    def generate_list(self, items, editable=False, prefix=None):
        if not prefix:
            raise ValueError("Prefix is required for list")
        style = self.get_inline_style(prefix + '-list')
        html = f'<ul id="{prefix}-list" class="{prefix}-list" style="{style}">\n'
        for i, item in enumerate(items):
            item_style = self.get_inline_style(prefix + '-item')
            if editable:
                html += f'    <li id="{prefix}-item-{i}" class="{prefix}-item" style="{item_style}"><input type="checkbox" name="{prefix}-item-{i}"> <span contenteditable="true">{item}</span></li>\n'
            else:
                html += f'    <li id="{prefix}-item-{i}" class="{prefix}-item" style="{item_style}">{item}</li>\n'
        html += '</ul>\n'
        return html

    # 生成表格
    def generate_table(self, headers, data, editable=False, prefix=None):
        if not prefix:
            raise ValueError("Prefix is required for table")
        table_style = self.get_inline_style(prefix + '-table')
        html = f'<table id="{prefix}-table" class="{prefix}-table" style="{table_style}">\n'
        
        # 表头
        html += '  <thead>\n    <tr id="{}-header" class="{}-header">\n'.format(prefix, prefix)
        th_style = self.get_inline_style(prefix + '-th')
        html += f'      <th id="{prefix}-select-all-th" class="{prefix}-th" style="{th_style}"><input type="checkbox" id="{prefix}-select-all"></th>\n'
        for header in headers:
            header_id = header.lower().replace(" ", "-")
            html += f'      <th id="{prefix}-th-{header_id}" class="{prefix}-th" style="{th_style}">{header}</th>\n'
        html += '    </tr>\n  </thead>\n'
        
        # 表体
        html += f'  <tbody id="{prefix}-body" class="{prefix}-body">\n'
        for i, row in enumerate(data):
            html += f'    <tr id="{prefix}-row-{i}" class="{prefix}-row">\n'
            td_style = self.get_inline_style(prefix + '-td')
            html += f'      <td id="{prefix}-td-{i}-select" class="{prefix}-td" style="{td_style}"><input type="checkbox" name="{prefix}-row-{i}"></td>\n'
            for cell in row:
                cell_id = cell.lower().replace(" ", "-")
                if editable:
                    html += f'      <td id="{prefix}-td-{i}-{cell_id}" class="{prefix}-td" style="{td_style}" contenteditable="true">{cell}</td>\n'
                else:
                    html += f'      <td id="{prefix}-td-{i}-{cell_id}" class="{prefix}-td" style="{td_style}">{cell}</td>\n'
            html += '    </tr>\n'
        html += '  </tbody>\n</table>\n'
        return html

    # 生成表单
    def generate_form(self, action, fields, prefix=None):
        if not prefix:
            raise ValueError("Prefix is required for form")
        form_style = self.get_inline_style(prefix + '-form')
        html = f'<form id="{prefix}-form" class="{prefix}-form" action="{action}" method="post" style="{form_style}; display:none;">\n'
        for field in fields:
            label = field.get('label', '')
            field_type = field.get('type', 'text')
            name = field['name']
            name_id = name.lower().replace(" ", "-")
            label_style = self.get_inline_style(prefix + '-label')
            if field_type == 'radio':
                html += f'  <label id="{prefix}-label-{name_id}" class="{prefix}-label" style="{label_style}">{label}</label><br>\n'
                for option in field['options']:
                    option_id = option.lower().replace(" ", "-")
                    input_style = self.get_inline_style(prefix + '-radio')
                    html += f'  <input id="{prefix}-radio-{name_id}-{option_id}" class="{prefix}-radio" type="radio" name="{name}" value="{option}" style="{input_style}">{option}<br>\n'
            else:
                attrs = ' '.join([f'{k}="{v}"' for k, v in field.items() if k not in ['label', 'type', 'name']])
                html += f'  <label id="{prefix}-label-{name_id}" class="{prefix}-label" style="{label_style}">{label}</label><br>\n'
                input_style = self.get_inline_style(prefix + '-input')
                html += f'  <input id="{prefix}-input-{name_id}" class="{prefix}-input" type="{field_type}" name="{name}" {attrs} style="{input_style}"><br>\n'
        btn_style = self.get_inline_style(prefix + '-btn')
        html += f'  <button id="{prefix}-save-btn" class="{prefix}-btn" type="button" onclick="save{prefix.capitalize()}()" style="{btn_style}">保存</button>\n'
        html += '</form>\n'
        return html

    # 生成按钮
    def generate_button(self, text, action=None, python_code=None, prefix=None):
        if not prefix:
            raise ValueError("Prefix is required for button")
        btn_id = text.lower().replace(" ", "-")
        btn_style = self.get_inline_style(prefix + '-btn')
        html = f'<button id="{prefix}-{btn_id}" class="{prefix}-btn" style="{btn_style}">{text}</button>\n'
        if python_code:
            js_code = self.python_to_js(python_code)
            html = html.replace('>', f' onclick="{js_code}">')
        elif action:
            html = html.replace('>', f' onclick="{action}()">')
        return html

    # 将Python代码转换为JS代码的辅助函数（占位符）
    def python_to_js(self, python_code):
        return python_code  # 简化示例；根据需要实现

    # 生成HTML元素
    def generate_element(self, element):
        elem_type = element['type']
        prefix = element.get('prefix')
        if not prefix:
            raise ValueError(f"Prefix is required for element type: {elem_type}")
        
        html = ''
        if elem_type == 'list':
            editable = element.get('editable', False)
            html = self.generate_list(element['items'], editable, prefix)
        elif elem_type == 'table':
            editable = element.get('editable', False)
            html = self.generate_table(element['headers'], element['data'], editable, prefix)
        elif elem_type == 'form':
            html = self.generate_form(element['action'], element['fields'], prefix)
        elif elem_type == 'button':
            html = self.generate_button(element['text'], element.get('action'), element.get('python_code'), prefix)
        elif elem_type == 'paragraph':
            p_style = self.get_inline_style(prefix + '-p')
            html = f'<p id="{prefix}-p" class="{prefix}-p" style="{p_style}">{element["text"]}</p>\n'
        elif elem_type == 'image':
            img_style = self.get_inline_style(prefix + '-img')
            html = f'<img id="{prefix}-img" class="{prefix}-img" src="{element["src"]}" alt="{element.get("alt", "image")}" style="{img_style}">\n'
        elif elem_type == 'link':
            a_style = self.get_inline_style(prefix + '-a')
            html = f'<a id="{prefix}-a" class="{prefix}-a" href="{element["href"]}" style="{a_style}">{element["text"]}</a>\n'
        elif elem_type == 'hr':
            hr_style = self.get_inline_style(prefix + '-hr')
            html = f'<hr id="{prefix}-hr" class="{prefix}-hr" style="{hr_style}">\n'
        elif elem_type.startswith('h') and elem_type[1:].isdigit():
            level = elem_type[1:]
            h_style = self.get_inline_style(prefix + '-h' + level)
            html = f'<h{level} id="{prefix}-h{level}" class="{prefix}-h{level}" style="{h_style}">{element["text"]}</h{level}>\n'
        elif elem_type == 'blockquote':
            quote_style = self.get_inline_style(prefix + '-quote')
            html = f'<blockquote id="{prefix}-quote" class="{prefix}-quote" style="{quote_style}">{element["text"]}</blockquote>\n'
        elif elem_type == 'code':
            pre_style = self.get_inline_style(prefix + '-pre')
            html = f'<pre id="{prefix}-pre" class="{prefix}-pre" style="{pre_style}"><code>{element["text"]}</code></pre>\n'

        if 'children' in element:
            children_html = ''
            for child in element['children']:
                children_html += self.generate_element(child)
            if '{children}' in element.get('text', ''):
                html = html.replace('{children}', children_html)
            else:
                html = html.rstrip('\n') + children_html + '\n'

        return html

    # 生成HTML的主函数
    def generate_html(self):
        html = f"""<!DOCTYPE html>
<html>
<head>
  <title>{self.page_dict["title"]}</title>
</head>
<body>
"""
        # 头部
        if self.layout.get('show_header', True):
            header_style = self.get_inline_style('header')
            html += f'  <div id="header" class="header" style="{header_style}">{self.page_dict["header"]}</div>\n'

        # 侧边栏
        if self.layout.get('show_sidebar', True) and 'sidebar' in self.page_dict:
            sidebar_style = self.get_inline_style('sidebar')
            html += f'  <div id="sidebar" class="sidebar" style="{sidebar_style}">\n'
            html += self.generate_sidebar(self.page_dict['sidebar'], 'sidebar')
            html += '  </div>\n'

        # 内容区域
        content_style = self.get_inline_style('content')
        html += f'  <div id="content" class="content" style="{content_style}">\n'
        for element in self.page_dict['content']:
            html += self.generate_element(element)
        html += '  </div>\n'

        # JavaScript脚本
        if 'scripts' in self.page_dict:
            html += '  <script>\n'
            for script in self.page_dict['scripts']:
                html += f'    {script}\n'
            html += '  </script>\n'

        html += '</body>\n</html>'
        return html