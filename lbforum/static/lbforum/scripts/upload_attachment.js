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
        data: {'pk':p.parent().attr('id').split('_')[1], 'descn':p.children('.fld-descn').val()},
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
        data: {'pk':a_id},
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
    var id = p.attr('id').replace('attachment_', '');
    var fn = p.children(".filename").html();
    if (isImg(fn)) {
      f = '[attachimg]' + id + '[/attachimg]';
    } else {
      f = '[attach]' + id + '[/attach]';
    }
    $.markItUp( { replaceWith:f } );
  });

  //avoid repeat binding
  $('#uploaded_files .nb').removeClass('nb');
}

function add_attachment(attachment) {
  var html = tmpl("attachment_li_tmpl", attachment);
  $($.parseHTML(html)).appendTo('#uploaded_files');
  $('<input type="hidden" value="' + attachment.pk + '" name="attachments"/>').appendTo('#hidden_fields')
  bind();
}

$(function() {
  function initAttachUpload() {
    $('#fileInput').fileupload({
        url: URL_UPLOAD_ATTACH,
        dataType: 'json',
        add: function (e, data) {
          data.submit();
        },
        progress: function (e, data) {
          var radio = parseInt(data.loaded / data.total * 100, 10);
          $('.finished-radio', data.li).text(radio + '%');
        },
        done: function (e, data) {
          var attch = data.result.file;
          add_attachment(attch);
        }
    });
  }
  initAttachUpload();
  bind();
});

