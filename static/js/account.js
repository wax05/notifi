$("#submit").click(function(){
    var name = $("#user_name").val();
    var id = $("#user_id").val();
    var pw = $("#pw_input").val();
    var pw_check = $("#pw_check").val();
    var email = $("#email").val();
    var code = $("#code").val();
    if (pw == pw_check) {
        postdata = {//send data to server
            'name':name,
            'id':id,
            'pw':pw,
            'email':email,
            'code':code
        }
        $.ajax({
            type: 'POST',
            url: '/notifi/account',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(data){
                console.log(data);
                var res = data.sta;
                if (res == true) {
                    alert('회원가입이 정상적으로 처리되었습니다');
                    location.replace('/notifi/login');
                } else {
                    if (data.why == 'SQL ERROR') {
                        alert('서버에 오류가 발생했습니다 조금뒤에 시도해주세요');
                    } else if (data.why == 'code not match') {
                        alert('코드가 맞지 않습니다');
                        $("#code").val('');
                    } else {
                        alert('ID가 중복되었습니다')
                        $("#user_id").val('');
                    }
                }
            },
            error: function(request, status, error){
                alert('에러가 발생했습니다')
            }
        });
    } else {
        var pw = $("#pw_input").val('');
        var pw_check = $("#pw_check").val('');//틀리면 값 null로 바꿈
    }
    console.log(postdata);
});