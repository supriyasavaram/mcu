
const sortbyform = document.getElementById('sortbyform')
const sortbyselectionbox = document.getElementById('sortoptions')
const movlist = document.getElementById('movieslist')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

//console.log(csrf)

sortbyform.addEventListener('submit', function(event){
    event.preventDefault();
    display_sort();
}, false);

function display_sort(){
    var strsortby = sortbyselectionbox.options[sortbyselectionbox.selectedIndex].value
    $.ajax({
        url: "/movies/",
        type: "POST",
        data: {sortby:strsortby, csrfmiddlewaretoken: window.CSRF_TOKEN},

        success:function(response){
            console.log("SUCCESS!")
            $('#movieslist').html(response)
        }
    });
};

console.log(sortbyform)