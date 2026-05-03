from django import forms


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css_class = "input"
            if isinstance(widget, forms.Textarea):
                css_class = "input input--textarea"
                widget.attrs.setdefault("rows", 4)
            elif isinstance(widget, forms.CheckboxInput):
                css_class = "input input--checkbox"
            elif isinstance(widget, (forms.SelectDateWidget,)):
                css_class = "input"
            elif isinstance(widget, (forms.DateInput, forms.DateTimeInput)):
                widget.input_type = "date"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css_class}".strip()
