
function deletePost(postId) { if (confirm("정말로 이 게시물을 삭제하시겠습니까?")){
    $.ajax({
      type: "POST",
      url: '/delete_post/' + postId,
      data: { 
        'id' : $(".board_button btn btn-secondary btn-sm rounded-pill").val(),
      },
      
      success: function (data) {
        alert("삭제에 성공하였습니다.");
        location.reload();
      },
      error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr);
        if(xhr.status == 403) {
            alert("글 작성자만 삭제 가능합니다.");
        }
      }
    });
  }}
