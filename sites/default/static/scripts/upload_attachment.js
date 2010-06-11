function bind() {
	$('#uploaded_files .nb .descn').click(function() {
		$(this).next().toggle();
	});		
	$('#uploaded_files .nb .submit-descn').click(function() {
		var sm = $(this);
		var p = sm.parent();
		var ext = p.parent().children(".ext");
		$.ajax({
				type: 'POST',
				url: url_attachments_ajax_change_descn,
				data: {'id':p.parent().attr('id').split('_')[1], 'descn':p.children('.fld-descn').val()},
				dataType: 'json',
				beforeSend: function(){
					ext.html('&nbsp;');
					sm.after('<span class="ajax-loader"></span>');
					sm.toggle();
				},
				complete: function(){
					sm.next().remove();
					sm.toggle();
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					alert('fail.');
				},
				success: function(data, textStatus) {
					if (data.valid) {
						p.toggle();
					} else {
						ext.html(data.errors);
					}
				},
				'':''
		})
		return false;
	});		
	$('#uploaded_files .nb .remove').click(function() {
		var rm = $(this);
		var p = rm.parent();
		var fn = p.children(".filename").html();
		var ext = p.children(".ext");
		var a_id = p.attr('id').split('_')[1];
		$.ajax({
				type: 'POST',
				url: url_attachments_ajax_delete,
				data: {'id':a_id},
				dataType: 'json',
				beforeSend: function(){
					ext.html('&nbsp;');
					ext.addClass('ajax-loader');
					rm.toggle();
				},
				complete: function(){
					ext.removeClass('ajax-loader');
					rm.toggle();
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					alert('fail.');
				},
				success: function(data, textStatus) {
					if (data.valid) {
						p.empty();
						p.append('<span class="removed-fn">' + fn + '</span>');
						$('input[name$="attachments"][value$="' + a_id +'"]').remove();
					} else {
						ext.html(data.errors);
					}
				},
				'':''
		})
	});
	$('#uploaded_files .nb .insert').click(function() {
		var p = $(this).parent();
		var f = p.children(".filename").attr("href");
		var fn = p.children(".filename").html();
		if (isImg(f)) {
			f = '[img]' + f + '[/img]';
		} else {
			f = '[url=' + f + ']' + fn + '[/url]';
		}
		$.markItUp( { replaceWith:f } );
	});

	//avoid repeat binding
	$('#uploaded_files .nb').removeClass('nb');
}

function add_attachment(attachment) {
    $(tmpl("attachment_li_tmpl", attachment)).appendTo('#uploaded_files');
    $('<input type="hidden" value="' + attachment.id + '" name="attachments"/>').appendTo('#hidden_fields')
    bind();
}

$().ready(function() {
	var upload_btn = $("#upload_button");
	new AjaxUpload('upload_button', {
			action: url_attachments_ajax_upload,
			responseType: 'json',
			name: 'file',
			onSubmit : function(file, ext){
				upload_btn.text('Uploading');
				this.disable();
				interval = window.setInterval(function(){
					var text = upload_btn.text();
					if (text.length < 13){
						upload_btn.text(text + '.');					
					} else {
						upload_btn.text('Uploading');				
					}
				}, 200);
			},
			onComplete: function(file, response){
				upload_btn.text('Upload');
				window.clearInterval(interval);
				this.enable();
				if (response.valid) {
					add_attachment(response.attachment);
				} else {
				}
			}
	});
	bind();
});
