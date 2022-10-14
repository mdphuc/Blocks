function edit_comment(postID, commentID){
  let cmt = document.getElementById(`comment-edited-${postID}-${commentID}`)
  let entry = {
    text : cmt.value 
  }

  fetch(`${window.origin}/edit_comment/${postID}/${commentID}`, {
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
      
      document.getElementById(`cmt-${commentID}`).innerHTML = 
      `<a  href="/dashboard/${data["author_id"]}" style="color: black;font-size: large; text-decoration: none;"><img src="/static/${data["author_img_path"]}" style="width: 35px; clip-path: circle()"><b> ${data["author"]} </b></a>: ${data["text"]}`
      
      document.getElementById(`comment-edited-${postID}-${commentID}`).value = ""
      
      

    })
  })
}