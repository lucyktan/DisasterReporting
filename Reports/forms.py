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

types_of_residence=['','Single Family','Multi-Family','Manufactured Housing Unit']
types_of_occupancy=['','Own as primary residence','Rent as primary residence','Non-primary residence']
types_of_disaster=['','Flooding','Tornado','Hurricane/Tropical Storm','Earthquake']
yes_no_unsure=['','Yes','No','Unsure']
yes_no=['', 'Yes', 'No']
water_levels=['','Not present','Less than 3 inches','Between 3 inches and 18 inches','Above 18 inches']
class DisasterForm(forms.Form):
    first_name=forms.CharField(label='First Name',max_length=100)
    last_name=forms.CharField(label='Last Name',max_length=100)
    street_address=forms.CharField(label='Street Address',max_length=100)
    address_line_2=forms.CharField(label='Address Line 2',max_length=100,required=False)
    city=forms.CharField(label='City',max_length=100)
    state=forms.ChoiceField(label='State',choices=[(x,x) for x in sorted(states)])
    zipcode=forms.DecimalField(label='Zipcode',max_digits=5,decimal_places=0)
    type_of_residence=forms.ChoiceField(label='Type of Residence',choices=((x,x) for x in types_of_residence))
    type_of_occupancy=forms.ChoiceField(label='Type of Occupancy',choices=((x,x) for x in types_of_occupancy))
    type_of_disaster=forms.ChoiceField(label='Type of Disaster',choices=((x,x) for x in types_of_disaster))
    date_of_disaster=forms.DateField(label='Date of Disaster',initial=datetime.date.today,widget=forms.SelectDateWidget(years=(datetime.date.today().year-2,datetime.date.today().year-1,datetime.date.today().year)))
    insured=forms.ChoiceField(label='Residence is insured',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    mortgage=forms.ChoiceField(required=False, label='Residence carries a mortgage',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    owned_less_than_30_years=forms.ChoiceField(required=False, label='Residence has been owned by you for less than 30 years',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    predisaster_value=forms.DecimalField(label='Predisaster value of residence',decimal_places=2)

    water_damage=forms.ChoiceField(label='Is there water damage in your home?', choices=((i,yes_no[i]) for i in range(len(yes_no))))

    water_mobilehome=forms.ChoiceField(label='Do you have a mobile home?',choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_mobilehome_minor=forms.ChoiceField(required=False, label='Is water level less than 6 inches deep on the floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_mobilehome_major_plywood=forms.ChoiceField(required=False, label='Do you have plywood flooring in your mobile home?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_mobilehome_major_plywood_yes=forms.ChoiceField(required=False, label='Is water between 6 inches to 2 feet deep on the plywood floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_mobilehome_major_nonplywood=forms.ChoiceField(required=False, label='Is water between 1 inch to 2 feet deep on your nonplywood floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_mobilehome_destroyed=forms.ChoiceField(required=False, label='Is water greater than 2 feet deep on your floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))

    water_conventionalhome_minor=forms.ChoiceField(required=False, label='Is water between 2 and 3 inches on your first floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_conventionalhome_major=forms.ChoiceField(required=False, label='Is water between 3 inches and 5 feet on your first floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))
    water_conventionalhome_destroyed=forms.ChoiceField(required=False, label='Is water greater than 5 feet on your first floor?', choices=((i,yes_no[i]) for i in range(len(yes_no))))

    # normal_water=forms.ChoiceField(required=False, label='Water level on the first floor (non-basement) is',choices=((x,x) for x in water_levels))

    # normal_destroyed_0=forms.ChoiceField(required=False, label='Structure is permanently uninhabitable',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_destroyed_1=forms.ChoiceField(required=False, label='There is a complete failure of two or more major structural components (e.g., collapse of basement walls/foundation, walls, or roof)',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_destroyed_2=forms.ChoiceField(required=False, label='Only the foundation remains',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_destroyed_3=forms.ChoiceField(required=False, label='Structure will require demolition or removal by local or government because of disaster-related health and safety concerns',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))

    # normal_major_0=forms.ChoiceField(required=False, label='Failure of structural elements of the residence (e.g., walls, roof, floors, foundation, etc.) that are repairable',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_major_1=forms.ChoiceField(required=False, label='Residence is currently uninhabitable and will take more than 30 days to repair',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_major_2=forms.ChoiceField(required=False, label='Water covers electrical outlets',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_major_3=forms.ChoiceField(required=False, label='Water has compromised the structural integrity of the residence',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))

    # normal_minor_0=forms.ChoiceField(required=False, label='Residence is currently uninhabitable but can be made habitable in less than 30 days',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_minor_1=forms.ChoiceField(required=False, label='There is damage to functional components (i.e. furnace, water heater, HVAC, etc.)',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_minor_2=forms.ChoiceField(required=False, label='There is damage, or disaster related contamination, to private well or septic system',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # normal_minor_3=forms.ChoiceField(required=False, label='Windows or doors are unsecured due to damage',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))


    # manufactured_destroyed_0=forms.ChoiceField(required=False, label='The residence cannot be made habitable again, even with extensive repairs',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_destroyed_1=forms.ChoiceField(required=False, label='The residence\'s frame is bent, twisted, or otherwise compromised',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_destroyed_2=forms.ChoiceField(required=False, label='There is at least 12 inches of standing water',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_destroyed_3=forms.ChoiceField(required=False, label='The residence is missing the roof or has sustained significant damage to the roof covering, sheathing, and framing',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))

    # manufactured_major_0=forms.ChoiceField(required=False, label='The residence is not currently habitable but can be made habitable again with extensive repairs',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_major_1=forms.ChoiceField(required=False, label='Structural components of the residence (including windows, doors wall coverings, roof, bottom board insulation, and ductwork) are damaged',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_major_2=forms.ChoiceField(required=False, label='Water impacts the floor system',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_major_3=forms.ChoiceField(required=False, label='Water is up to 12 inches in a living area',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))

    # manufactured_minor_0=forms.ChoiceField(required=False, label='The residence is not currently habitable but can be made habitable again with few repairs',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_minor_1=forms.ChoiceField(required=False, label='Structural components of the residence (including windows, doors wall coverings, roof, bottom board insulation, and ductwork) have minor damage',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_minor_2=forms.ChoiceField(required=False, label='Water level is below the floor system',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))
    # manufactured_minor_3=forms.ChoiceField(required=False, label='The HVAC is damaged by water',choices=((i,yes_no_unsure[i]) for i in range(len(yes_no_unsure))))

    model = Report 
