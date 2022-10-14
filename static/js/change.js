document.getElementById('post_view').style.display = 'block'
document.getElementById('about_view').style.display = 'none'
document.getElementById('friend_view').style.display = 'none'

function change1(){
  document.getElementById('post_view').style.display = 'block'
  document.getElementById('about_view').style.display = 'none'
  document.getElementById('friend_view').style.display = 'none'

  document.getElementById('post').className = "button1-change"
  document.getElementById('about').className = "button1"
  document.getElementById('friend').className = "button1"

}

function change2(){
  document.getElementById('post_view').style.display = 'none'
  document.getElementById('about_view').style.display = 'block'
  document.getElementById('friend_view').style.display = 'none'

  document.getElementById('post').className = "button1"
  document.getElementById('about').className = "button1-change"
  document.getElementById('friend').className = "button1"
}

function change3(){
  document.getElementById('post_view').style.display = 'none'
  document.getElementById('about_view').style.display = 'none'
  document.getElementById('friend_view').style.display = 'block'

  document.getElementById('post').className = "button1"
  document.getElementById('about').className = "button1"
  document.getElementById('friend').className = "button1-change"
}

function change4(){

  document.getElementById('post').className = "button1"
  document.getElementById('about').className = "button1"
  document.getElementById('friend').className = "button1"
}