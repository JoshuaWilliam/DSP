""" All SSML Sentences per personality type are contained in a dictionary for each intent"""

intent_dict = {
    'extravert': {
        'greet': 'Good morning! I hope you had a good night.\n'
                 'As Carrie Snow always says, “No day is so bad it can’t be fixed with a nap.”',
        'control-lights-on': 'The lights are on, so let it shine!',
        'to-do': 'It seems like the only thing you have on your schedule today is your mother\'s birthday at 2 o\'clock. \n Enjoy the party!',
        'meditate': 'I\'ve already prepared a default meditation session for you!\n'
                    'Enjoy a moment of peace!',
        'weather': 'It is a beautiful day today!\n'
                   '20 degrees, so...pull out you shorts!',
        'traffic': 'There is a jam on the A20, so you better take the N1 if you want to get to your mother\'s birthday on time!',
        'peptalk': 'You know you can do this, you are amazing!',
        'control-lights-off':  'Let there be darkness...',
        'part': 'So long, old friend!\n'
                'Until next time.'
        # 'part': 'So long, old friend! Until next time.'
    },

    'introvert': {
        'greet': 'Good morning, I hope you slept well.',
        'control-lights-on': 'The lights are now on.',
        'to-do': 'You have one event on your schedule today, your mother\'s birthday at 2 o\'clock.',
        'meditate': 'Your meditation session is ready to start.',
        'weather': 'Today is probably going to be a sunny day, with 20 degrees.',
        'traffic': 'There seems to be a traffic jam on the A20.\n'
                   'Maybe you should take you take the N1 to avoid being late',
        'peptalk': 'I\'ve heard that energy and persistence conquer all things.\n'
                   'If you think positively, you will succeed!',
        'control-lights-off': 'The lights are now off.',
        'part': 'Good bye.'
    }
}
