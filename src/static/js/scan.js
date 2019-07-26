function simple_scan() {
  var network = $("#network-to-scan").val();

  const request = $.ajax({
    type: "POST",
    url: "/api/simple-scan",
    contentType: "application/json",
    data: JSON.stringify({"iprange":network}),
    dataType:"json"});

  request.done(msg => {
    alert(msg.msg)
  });
}
