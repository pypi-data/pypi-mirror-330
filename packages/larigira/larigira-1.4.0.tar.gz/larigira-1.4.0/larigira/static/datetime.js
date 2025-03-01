/* global webshim */
webshim.setOptions('forms-ext', {
  'types': 'datetime-local',
  'datetime-local': {
    'classes': 'show-uparrow inputbtns-outside',
    'openOnFocus': false,
    'yearSelect': true,
    'stepfactor': 60
  }
})
webshim.polyfill('forms-ext')
