function bind() {
	$('#uploaded_files .descn').click(function() {
		$(this).next().toggle();
	});		
	$('#uploaded_files .submit-descn').click(function() {
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
	$('#uploaded_files .remove').click(function() {
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
}
$().ready(function() {
	$("#id_message").markItUp(mySettings);
	new AjaxUpload('upload_button', {
			action: url_attachments_ajax_upload,
			responseType: 'json',
			name: 'file',
			onComplete: function(file, response){
				if (response.valid) {
					$(tmpl("attachment_li_tmpl", response.attachment)).appendTo('#uploaded_files');
					$('<input type="hidden" value="' + response.attachment.id + '" name="attachments"/>').appendTo('#hidden_fields')
					bind();
				} else {
				}
			}
	});
	bind();
});
