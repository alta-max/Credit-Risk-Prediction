function search_element()
{
  var i,td,txtValue;
  var search_input = document.querySelector('#search_id');
  var filter = search_input.value.toUpperCase();
  var table = document.querySelector("#csvRoot");
  var tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

