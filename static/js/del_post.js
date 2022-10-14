function del_post(postID){
  let entry = {
    function : "delete-post" 
  }

  fetch(`${window.origin}/delete_post/${postID}`, {
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
      
      document.getElementById(`${postID}`).remove()
      
      

    })
  })
}
