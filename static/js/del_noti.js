function del_noti(notiID){
  let entry = {
    function : "delete_notification"
  }

  fetch(`${window.origin}/delete_notification/${notiID}`, {
    method: 'POST',
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type" : "application/json"
    })
  }).then(function(response){
    if (response.status !== 200){
      console.log(`Failed : ${response.status}`)
      return
    }

    response.json().then(function(data){
      if(data["state"] == "authorized"){
        document.getElementById(`${notiID}`).remove()
        document.getElementById(`del-${notiID}`).remove()
        
      }else{
        document.getElementById("error-alert").style.display = "block"
      }
      

    })
  })
}


