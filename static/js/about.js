function about(userID){
  let about = document.getElementById(`about_text`)
  let entry = {
    text : about.value 
  }

  fetch(`${window.origin}/about/${userID}`, {
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
      document.getElementById(`about_display`).innerHTML = data["text"]
      document.getElementById(`about_display`).title = data["date_created"]
      document.getElementById('about_text').value = ""
      
      

    })
  })
}