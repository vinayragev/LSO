function get_star(num) {
star = ''
for (var i = 0; i < 5; i++) {
  if (num>i) {
    star += '<i class="fa fa-star" aria-hidden="true"></i>'
  }else{
    star += '<i class="fa fa-star-o" aria-hidden="true"></i>'
  }
}
return star;
}
function toLocaleString(str){
	if (str) {
		return str.toLocaleString()
	}
	return 0
}
function update_geolocation(){
	$('.spinner-border').show()
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (argument) {
        	cur_location = argument;
			$('.spinner-border').hide()
            setCookie("latitude",argument.coords.latitude)
            setCookie("longitude",argument.coords.longitude)
            console.log("location added")
        });
    }
}
function get_average_rgb(img) {
    var context = document.createElement('canvas').getContext('2d');
    if (typeof img == 'string') {
        var src = img;
        img = new Image;
        img.setAttribute('crossOrigin', ''); 
        img.src = src;
    }
    context.imageSmoothingEnabled = true;
    context.drawImage(img, 0, 0, 1, 1);
    return context.getImageData(0, 0, 1, 1).data.slice(0,3);
}
function capitalizeFirstLetter(str) {
	str = str.split(' ')
	newstr = ''
	for (var i = 0; i < str.length; i++) {
		if (str[i]!='') {
		 str[i] += str[i][0].toUpperCase() + str[i].slice(1)
		}
	}
    return str.join(' - ')
}
function replace_HTML(html,obj){
	obj_keys = Object.keys(obj)
	for (var i = 0; i < obj_keys.length; i++) {
		html = html.replaceAll(obj_keys[i],obj[obj_keys[i]])
	}
	return html
}
function input_GET(key){
	params = new URL(location.href)
	params = new URLSearchParams(params.search);
	return params.get(key)
}
function setCookie(name,value) {
    var expires = "";
    var date = new Date();
    date.setTime(date.getTime() + (30*24*60*60*1000));
    expires = "; expires=" + date.toUTCString();
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
function get_time(time){
    date = new Date(time)
    return date.toLocaleString('en-US', {hour:'numeric', minute:'numeric', second:'numeric', hour12: true })+', '+date.toDateString()
}
function get_time_diff(time_str){
	old = new Date(time_str)
	now = new Date()
	dif = (now-old)
	return_resp = []
	dif /= 1000
	switch(true){
		case dif>60*60*24*365: return_resp.push([parseInt(dif/(60*60*24*365)),'Y']);dif %= (60*60*24*365)
		case dif>60*60*24*31:  return_resp.push([parseInt(dif/(60*60*24*31)),'M']);dif %= (60*60*24*31)
		case dif>60*60*24:     return_resp.push([parseInt(dif/(60*60*24)),'D']);dif %= (60*60*24)
		case dif>60*60:        return_resp.push([parseInt(dif/(60*60)),'H']);dif %= (60*60)
		case dif>60:           return_resp.push([parseInt(dif/(60)),'M']);dif %= (60)
		default:               return_resp.push([parseInt(dif),'S']);
	}
	return return_resp
}
function get_img_src(src){
	if (src) {
		if (src.indexOf('https:')===0) { 
			return src
		}
		return location.origin+globalThis.STATIC_URL+src.trim()
	}
	return ''
}
function custom_AJAX(obj,file=false) {
	obj['DATA']['csrfmiddlewaretoken'] = globalThis.csrfmiddlewaretoken
	obj['DATA']['language'] = 'english'
	obj['DATA']['longitude'] = getCookie('longitude')
	obj['DATA']['latitude'] = getCookie('latitude')

	$('.ajax-message').html('').closest('.ajax-message-div').hide()
	ajaxObject = {
		success:function (response) {
			console.log(response)
			// if (typeof(response.user) !=='undefined' && $('.user_name').html()!===response.user.name) {
			// if (typeof(response.user) !=='undefined') {
			// 	$('.user_name').html(response.user.name)
			// }
			obj['SUCCESS'](response)
			if (response.message) {
				$('.ajax-message').html(response.message).closest('.ajax-message-div').show()
				if (response.success) {
					$('.ajax-message').closest('.alert-dismissible').removeClass('alert-danger').addClass('alert-success')
				}else{
					$('.ajax-message').closest('.alert-dismissible').removeClass('alert-success').addClass('alert-danger')
				}
			}
		},
	    error: function (jqXHR, exception) {
	        console.log(jqXHR.statusText);
	    }
	}
	ajaxObject['dataType'] = 'JSON'
	ajaxObject['url']      = obj['URL']
	ajaxObject['type']     = obj['TYPE']
	if (file) {
		DATA_keys = Object.keys(obj['DATA'])
		formData = new FormData()
		for (var i = 0; i < DATA_keys.length; i++) {
			formData.append(DATA_keys[i],obj['DATA'][DATA_keys[i]]) 
		}
		ajaxObject['data']         = formData
        ajaxObject['async']        =  true
        ajaxObject['cache']        =  false
        ajaxObject['contentType']  =  false
        ajaxObject['processData']  =  false
        ajaxObject['timeout']      =  60000
	}else{
		ajaxObject['data']     = obj['DATA']
	}

	// object_keys = Object.keys(ajaxObject['data'])
	// for (var i = object_keys.length - 1; i >= 0; i--) {
	// 	ajaxObject['data'][i]
	// }
	$.ajax(ajaxObject)
}
$(document).ready(function () {
	switch(true){
		case location.pathname==='/admin/':
			$('[href="/admin/"]').addClass('active');break;
		default :
			$('[href="'+location.pathname+'"]').addClass('active').closest('.collapse').addClass('show').parent().closest('.collapse').addClass('show')
	}
})