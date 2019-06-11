from django import forms
from django.forms import Form
from .models import *
from io import BytesIO
from django.core.exceptions import ValidationError
import tempfile
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

TEAM_CHOICES = (("25_Rare", "Rare"),
                ("24_Ref", "Referee"),
                ("22_Volunteer", "Volunteer"),
                ("04_Austria", "Austria"),
                ("18_Belgium", "Belgium"),
                ("05_Catalonia", "Catalonia"),
                ("21_Comittee", "Comittee"),
                ("06_Czech", "Czech Republic"),
                ("19_Denmark", "Denmark"),
                ("07_Finland", "Finland"),
                ("03_France", "France"),
                ("02_Germany", "Germany"),
                ("08_Ireland", "Ireland"),
                ("09_Italy", "Italy"),
                ("17_Netherlands", "Netherlands"),
                ("01_Norway", "Norway"),
                ("10_Poland", "Poland"),
                ("16_Scotland", "Scotland"),
                ("20_Slovakia", "Slovakia"),
                ("11_Slovenia", "Slovenia"),
                ("23_Snitch", "Snitch"),
                ("12_Spain", "Spain"),
                ("13_Switzerland", "Switzerland"),
                ("14_Turkey", "Turkey"),
                ("15_UK", "UK"))

POSITION_CHOICES = (("Keeper", "Keeper"),
                    ("Chaser", "Chaser"),
                    ("Beater", "Beater"),
                    ("Seeker", "Seeker"),
                    ("Utility", "Utility"),
                    ("Speaking Captain", "Speaking Captain"),
                    ("Coach", "Coach"),
                    ("Team Captain", "Team Captain"),
                    ("Head Referee", "Head Referee"),
                    ("Assistant Referee", "Assistant Referee"),
                    ("Snitch Referee", "Snitch Referee"),
                    ("Snitch Runner", "Snitch Runner"),
                    ("Pitch Manager", "Pitch Manager"),
                    ("Merchandise", "Merchandise"),
                    ("Live Steam", "Live Stream"),
                    ("Commentator", "Commentator"),
                    ("Comittee", "Comittee"),
                    ("Volunteer", "Volunteer"),
                   )


class ImageDataField(forms.ImageField):
    def to_python(self, data):
        from base64 import b64decode
        if not data:
            raise ValidationError(self.error_messages['invalid_image'])
        f = tempfile.NamedTemporaryFile(suffix=".png")
        try:
            f.write(b64decode(data.split(',')[1]))
        except IndexError:
            raise ValidationError(self.error_messages['invalid_image'])
        from PIL import Image

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(f)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            f.image = image
            # Pillow doesn't detect the MIME type of all formats. In those
            # cases, content_type will be None.
            f.content_type = Image.MIME.get(image.format)
        except Exception as exc:
            # Pillow doesn't recognize it as an image.
            raise ValidationError(
                self.error_messages['invalid_image'],
                code='invalid_image',
            ) from exc
        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


class CardForm(Form):
    name = forms.CharField(label='Your name', max_length=20, help_text="Recommend below 10 characters")
    team = forms.ChoiceField(choices=TEAM_CHOICES)
    number = forms.CharField(label='Your number', max_length=2, required=False, validators=[
            RegexValidator(
                r'^[0-9]*$',
                'Only 0-9 and 00-99 are allowed.',
                'Invalid Number'
            ),
            MinLengthValidator(1),
            MaxLengthValidator(2),
        ],)
    phrase = forms.CharField(widget=forms.Textarea, max_length=100, help_text="Recommend below 56 characters", required=False)
    copy = forms.CharField(label='Copyright', help_text='Give credit, if the photographer wants it.', max_length=50, required=False)
    position = forms.MultipleChoiceField(choices=POSITION_CHOICES, help_text='Max. 3 positions, if all choose utility; choose multiple by holding Ctrl./Strg.')
    # func = forms.MultipleChoiceField(choices=FUNCTION_CHOICES, required=False,
    #                                      help_text='Max. 3 functions; choose multiple by holding Ctrl./Strg.')
    cata = forms.IntegerField(label='Kilometers traveled to Bamberg', min_value=0, max_value=9999, required=False)
    catb = forms.IntegerField(label='Sunburn Resistance (0-10)', min_value=-5, max_value=20, required=False)
    catc = forms.IntegerField(label='Traded Jerseys', min_value=0, max_value=999, required=False)
    catd = forms.IntegerField(label='Years of Quidditch', min_value=0, max_value=20, required=False)
    image = ImageDataField(widget=forms.HiddenInput)
