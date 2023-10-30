function EditPost(postId) { if (confirm("수정하시겠습니까")){
    $.ajax({
      type: "POST",
      url: '/edit/'+ postId,
      data: { 
        'id' : $(".btn btn-secondary").val(),
      },
      success: function (data) {
        location.href('/edit_process')
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr);
        if(xhr.status == 403) {
            alert("글 작성자만 수정 가능합니다.");
        }
      }
    });
  }}