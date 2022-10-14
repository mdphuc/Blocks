function del(postID, commentID){
  let entry = {
    function : "delete" 
  }

  fetch(`${window.origin}/delete_comment/${postID}/${commentID}`, {
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
      
      document.getElementById(`cmt-div-${commentID}`).remove()
      document.getElementById(`comment-edited-${postID}-${commentID}`).remove()
      
      

    })
  })
}