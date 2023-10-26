$(function() {
  // 监听发送消息按钮的点击事件
  $('#submit-button').click(sendMessage);

  // 监听输入框的键盘事件
  $('#user-input').keydown(function(e) {
    if (e.keyCode == 13 && !e.shiftKey) {
      e.preventDefault(); // 阻止默认行为（换行）
      sendMessage();
    }
  });

  // 发送消息到服务器并获取回复
  function sendMessage() {
    var message = $('#user-input').val().trim();
    if (message) {
      $.ajax({
        type: 'POST',
        url: '/chat',
        data: JSON.stringify({ message: message }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
          var reply = data['message'];
          $('#chat-display-window').append('<p><span class="user-message">' + message + '</span></p>');
          $('#chat-display-window').append('<p><span class="bot-message">' + reply + '</span></p>');
          $('#user-input').val('');
          $('#chat-display-window').scrollTop($('#chat-display-window')[0].scrollHeight);
        }
      });
    }
  }
});
