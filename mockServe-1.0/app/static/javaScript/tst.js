/**
 * Created by jinjie673 on 2018/1/1.
 */


$("#formSubmit").click( function() {
    $('#uploadFileForm').ajaxSubmit({
        url: "/uploadFile.do",
        type: "POST",
        dataType: "json",
        success: function (data) {
             if( data.message !='创建接口成功!'){
                 $('.page-header p').text(data.message);
             }else{
                  $('#uploadFileForm')[0].reset();
                  $('.page-header p').text("pleased to meet you");
                  alert( data.message );
             }
        },
        error: function (data) {
            alert("error:" + data.responseText);
        }
    });
});


function submitFormData(){
    $('#uploadFileForm').ajaxSubmit(function() {
        $.ajax({
            type: "POST",
            dataType: "JSON",
            success: function (data) {
                console.log(data);
                    },
            error: function(data) {
                alert("error:"+data.responseText);
                }
            });
        }
    );
}

function updateData(){
    $('#updateInterface').ajaxSubmit({
        url: "/updateInterFace.do",
        type: "POST",
        success: function(data){
            if (data = "修改接口成功"){
                alert( data);
                window.location.href = "/home.html";
            }
            else{
                $('.page-body p').text(data.message)
                }
            },
        error: function(data){
            alert("error:"+data.responseText);
        }
    })
}

function delint(dsInt){
    $.ajax({
        url: "/delIntId",
        type: "POST",
        data: {dsInt:dsInt},
        success: function (data) {
            if (data = "success") {
                alert("删除接口成功")
                window.location.reload()
            } else {
                alert("删除接口失败");
            }
        },
        error: function (data) {
            alert("error:" + data.responseText);
        }
    })
}

function changePage(){
    var num = $("#pageNumber").val();
    $.ajax({
        url:"/selectAll.do",
        type:"POST",
        data:{"pageNumber":num},
        dataType: "JSON",
        success:function(data){
            $(".table tbody").empty();
            for(var i in data ){
            var routetype =data[i].type;
                    if (routetype == "0"){
                        routetype = "http";
                    }else if (routetype == "1"){
                        routetype = "https";
                    }else{
                        routetype = "XML";
                    }
            var _tr =  '<tr>'+
            '<td>'+ data[i].routeUrl + '</td>'+
            '<td>'+ routetype + '</td>'+
            '<td>'+ data[i].creater + '</td>'+
            '<td>'+ data[i].createDate + '</td>'+
            '<td>'+
            '<a href="detail/intId='+data[i].routeUrl+'">'+ ck +'</a>'+
            '<a href="updateInt/intId='+data[i].routeUrl+'">'+ bj +'</a>'+
            '<font color="#337ab7">'+
            '<span id="delInterface" class="curStyle" onclick=delint("'+data[i].routeUrl+'") >' + sc + '</span>' +
            '</font>'+
            '</td>'+
            '</tr>';
            $("table").append(_tr);
            }
        }
    })
}

function addHtml(){
   var _html = '<div class="row">'+
       '<textarea class="upInputArea3" name="theKey" placeholder="关键词"></textarea>'+
       '<br>'+
       '<textarea class="upInputArea3" name="theValue" placeholder="关键词信息"></textarea>'+
       '<br>'+
       '<textarea class="upInputArea" name="res" placeholder="返回信息："></textarea>'+
       '<br>'+ '<br>'+
       '</div>';
    $("#logic").append(_html)
}

function delHtml(){
    var len = ($(".row")).length;
    if( len > 1 ){
        $(".row").eq(len-1).remove();
    }
}
