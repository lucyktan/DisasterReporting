"""The Report damage form"""

import datetime
from django import forms
from models import Report

states = ['',
         'Alaska',
         'Alabama',
         'Arkansas',
         'American Samoa',
         'Arizona',
         'California',
         'Colorado',
         'Connecticut',
         'District of Columbia',
         'Delaware',
         'Florida',
         'Georgia',
         'Guam',
         'Hawaii',
         'Iowa',
         'Idaho',
         'Illinois',
         'Indiana',
         'Kansas',
         'Kentucky',
         'Louisiana',
         'Massachusetts',
         'Maryland',
         'Maine',
         'Michigan',
         'Minnesota',
         'Missouri',
         'Northern Mariana Islands',
         'Mississippi',
         'Montana',
         'National',
         'North Carolina',
         'North Dakota',
         'Nebraska',
         'New Hampshire',
         'New Jersey',
         'New Mexico',
         'Nevada',
         'New York',
         'Ohio',
         'Oklahoma',
         'Oregon',
         'Pennsylvania',
         'Puerto Rico',
         'Rhode Island',
         'South Carolina',
         'South Dakota',
         'Tennessee',
         'Texas',
         'Utah',
         'Virginia',
         'Virgin Islands',
         'Vermont',
         'Washington',
         'Wisconsin',
         'West Virginia',
         'Wyoming'
]

types_of_residence=['Single Family','Multi-Family','Manufactured Housing Unit']
types_of_occupancy=['Own as primary residence','Rent as primary residence','Non-primary residence']
types_of_disaster=['Flooding','Tornado','Hurricane/Tropical Storm','Earthquake']
yes_no_unsure=['No', 'Yes', 'Unsure']
yes_no=['No', 'Yes']
water_levels=['','Not present','Less than 3 inches','Between 3 inches and 18 inches','Above 18 inches']
class DisasterForm(forms.Form):
    first_name=forms.CharField(label='First Name',max_length=100)
    last_name=forms.CharField(label='Last Name',max_length=100)
    street_address=forms.CharField(label='Street Address',max_length=100)
    address_line_2=forms.CharField(label='Address Line 2',max_length=100,required=False)
    city=forms.CharField(label='City',max_length=100)
    state=forms.ChoiceField(label='State',choices=[(x,x) for x in sorted(states)])
    zipcode=forms.CharField(label='Zipcode',max_length=5)
    type_of_residence=forms.ChoiceField(label='Type of Residence',choices=((x,x) for x in types_of_residence), widget=forms.RadioSelect)
    type_of_occupancy=forms.ChoiceField(label='Type of Occupancy',choices=((x,x) for x in types_of_occupancy), widget=forms.RadioSelect)
    type_of_disaster=forms.ChoiceField(label='Type of Disaster',choices=((x,x) for x in types_of_disaster), widget=forms.RadioSelect)
    date_of_disaster=forms.DateField(label='Date of Disaster',initial=datetime.date.today,widget=forms.SelectDateWidget(years=(datetime.date.today().year-2,datetime.date.today().year-1,datetime.date.today().year)))
    insured=forms.ChoiceField(label='Residence is insured', choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    mortgage=forms.BooleanField(required=False, label='Residence carries a mortgage')
    owned_less_than_30_years=forms.BooleanField(required=False, label='Residence has been owned by you for less than 30 years')
    predisaster_value=forms.DecimalField(label='Predisaster value of residence',decimal_places=2)

    water_damage=forms.BooleanField(label='Is there water damage in your home?')

    water_mobilehome=forms.BooleanField(label='Do you have a mobile home?')
    
    water_mobilehome_minor=forms.BooleanField(required=False, label='Is water level less than 6 inches deep on the floor?')
    
    water_mobilehome_major_plywood=forms.BooleanField(required=False, label='Do you have plywood flooring in your mobile home?')
    water_mobilehome_major_plywood_yes=forms.BooleanField(required=False, label='Is water between 6 inches to 2 feet deep on the plywood floor?')
    water_mobilehome_major_nonplywood=forms.BooleanField(required=False, label='Is water between 1 inch to 2 feet deep on your nonplywood floor?')
    water_mobilehome_destroyed=forms.BooleanField(required=False, label='Is water greater than 2 feet deep on your floor?')

    water_conventionalhome_minor=forms.BooleanField(required=False, label='Is water between 2 and 3 inches on your first floor?')
    water_conventionalhome_major=forms.BooleanField(required=False, label='Is water between 3 inches and 5 feet on your first floor?')
    water_conventionalhome_destroyed=forms.BooleanField(required=False, label='Is water greater than 5 feet on your first floor?')

    sewage = forms.BooleanField(required=True, label='Is there more than 1 foot of sewage in your home?')

    minor10_0 = forms.BooleanField(required=False, label='Are there broken windows?')     
    minor10_1 = forms.BooleanField(required=False, label='Is there damage to landscaping?')
    minor10_2 = forms.BooleanField(required=False, label='Is more than 50% of your home damaged?')

    major20_0 = forms.BooleanField(required=False, label='If you have a chimney, is it no longer functional?')
    major20_1 = forms.BooleanField(required=False, label='If you have a carpet on the first floor, is the majority of it soaked?')
    major20_2 = forms.BooleanField(required=False, label='If you have a parking lot, is it damaged?')

    major30_0 = forms.BooleanField(required=False, label='Is there damage from smoke?')
    major30_1 = forms.BooleanField(required=False, label='Is the fire escape inoperable?')
    major30_2 = forms.BooleanField(required=False, label='Are roof tiles missing?')
    major30_3 = forms.BooleanField(required=False, label='Are your vehicles damaged?')

    major40_0 = forms.BooleanField(required=False, label='Is there minor damage to interior flooring?')
    major40_1 = forms.BooleanField(required=False, label='Is there minor damage to exterior walling?')
    major40_2 = forms.BooleanField(required=False, label='Are there fallen trees on your home?')

    major50_0 = forms.BooleanField(required=False, label='Is there at least one room that is destroyed?')
    major50_1 = forms.BooleanField(required=False, label='Are any exits blocked?')
    major50_2 = forms.BooleanField(required=False, label='Are any utilities damaged? (furnace, water heater, well, septic system, etc)')

    major60_0 = forms.BooleanField(required=False, label='Is the foundation of your home damaged?')
    major60_1 = forms.BooleanField(required=False, label='Is the insulation in your home damaged')

    major74_0 = forms.BooleanField(required=False, label='Is the exterior frame of your home damaged?')
    major74_1 = forms.BooleanField(required=False, label='Is the roof off or collapsed?')
    major74_2 = forms.BooleanField(required=False, label='Are accessory outbuildings damaged?')

    destroyed80_0 = forms.BooleanField(required=False, label='Is there flooding above the first floor?')
    destroyed80_1 = forms.BooleanField(required=False, label='Did your home move off its foundation?')
    destroyed80_2 = forms.BooleanField(required=False, label='Did any walls collapse?')
    destroyed80_3 = forms.BooleanField(required=False, label='Is the structure permanently uninhabitable?')
    destroyed80_4 = forms.BooleanField(required=False, label='Does your home require demolition because it is in danger due to landslides, mudslides, sinkholes, beach erosion, etc?')

    destroyed90_0 = forms.BooleanField(required=False, label='Did your home level above the foundation?')
    destroyed90_1 = forms.BooleanField(required=False, label='Is the second floor of your home completely gone?')

    destroyed100_0 = forms.BooleanField(required=False, label='Is your home leveled above the foundation, and is the basement and foundation damaged?')
    destroyed100_1 = forms.BooleanField(required=False, label='Is there flooding above the eaves (edge of the roof)?')

    model = Report 

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

