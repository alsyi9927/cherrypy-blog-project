  function EditPost(id) {
    if (confirm("수정하시겠습니까?")) {
      $.ajax({
        type: "POST",
        url: '/edit',
        data: {
          'id': $("#inputID").val(),
          'title' :$("#inputTitle").val(),
          'content' :$("#inputContent").val(),
        },
        success: function (data) {
          console.log('수정 성공');
          location.href = '/dashboard';
        },
      });
    }
  }
  