var config = {
  '.chosen-select'           : {max_selected_options:1},
  '.chosen-select-deselect'  : { allow_single_deselect: true },
  '.chosen-select-no-single' : { disable_search_threshold: 10 },
  '.chosen-select-no-results': { no_results_text: 'Oops, nothing found!' },
  '.chosen-select-rtl'       : { rtl: true },
  '.chosen-select-width'     : { width: '95%' }
}
$('.chosen-select').chosen({ width: '100%',no_results_text: 'Oops, nothing found!'  });
// for (var selector in config) {
//   $(selector).chosen(config[selector]);
// }
