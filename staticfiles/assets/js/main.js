// $("body").flurry({
//   character: ["❄", "❅", "❆", "❉", "❊"],
//   color: ["#55476A", "#AE3D63", "#DB3853", "#F45C44", "#F8B646"],
//   speed: 3000,
//   height: 480,
//   frequency: 60,
//   small: 12,
//   large: 50,
//   rotation: 90,
//   rotationVariance: 20,
//   startRotation: 90,
//   wind: 300,
//   windVariance: 100,
//   opacityEasing: "cubic-bezier(1,0,.96,.9)",
// });

$(window).scroll(function () { 
  if($(this).scrollTop() > 100){
    $(".navb").addClass("bg-light");
  }else{
    $(".navb").removeClass("bg-light");
  }
});


$(".add-to-cart").click(function (e) {
  e.preventDefault();
  var productImage = $(this).data("product-image");
  var name = $(this).data("name");
  var deletedPrice = $(this).data("price");
  var sellingPrice = $(this).data("selling-price");
  var slug = $(this).data("slug");

  $("#productImage").attr("src", productImage);
  $("#productName").text(name);
  $("#productDeletedPrice").text(deletedPrice);
  $("#sellingPrice1").text(sellingPrice);
  $("#viewBtn").attr("onclick", `window.location.href='/product/${slug}'`);
});

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

$("#searchInput").keyup(function (e) {
  $("#searchOutput").text("Searching...");

  $.ajax({
    type: "get",
    url: "/search?q=" + $(this).val(),
    dataType: "json",
    success: function (response) {
      response.products.forEach((element) => {
        console.log(response.products);
        $("#searchOutput")
          .html(`<div class="bg-white shadow-sm rounded p-2 col-md-4 d-flex gap-3">
          <img src="/media/${element.thumbnail}" width="80px" alt="">
          <div class="align-self-center">
              <h6>${element.name}</h6>
              <p><span>Rs. ${element.price}</span></p>
              <a href="/product/${element.slug}" class="btn btn-sm btn-dark">View</a>
          </div>
      </div>`);
      });

      if(response.products.length == 0){
        $("#searchOutput").text("Not Found...");

      }
    },
    error: function () {
      $("#searchOutput").text(`Not found`);
    },
  });
});

const popoverTriggerList = document.querySelectorAll(
  '[data-bs-toggle="popover"]'
);
const popoverList = [...popoverTriggerList].map(
  (popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl)
);

const toastElList = [].slice.call(document.querySelectorAll('.toast'))
const toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl)
})
toastList.forEach(toast => toast.show());

function updateCart() {
  $.ajax({
    type: "get",
    url: "/cart/get",
    data: "json",
    success: function (response) {
      $("#cartCount").text(response.products.length);
      $("#total").text(response.total);
      $("#items").html(""); // Clear the items container
      response.products.forEach((element) => {
        $("#items").append(
          `<div class="bg-white shadow-sm rounded d-flex gap-2">
          <img src="${element.thumbnail}" width="100px" class="p-1" >
          <div class="p-2">
              <span class="text-dark fs-6">${element.name}</span> <br>
              <small class="text-underline">Rs. ${element.price}</small>
              <div class="d-flex pt-3 border-dark rounded gap-2 align-items-center justify-content-between">
               <div class="d-flex gap-2">
                <button class="cart-btn decrease-quantity" data-id="${element.id}">-</button>
                <span class="px-2">${element.quantity}</span>
                <button class="cart-btn increase-quantity" data-id="${element.id}">+</button>
               </div>
                <button class="cart-btn bg-danger delete-item" data-id="${element.id}"><i class="ti ti-trash fs-6"></i></button>
              </div>
          </div>
          </div>`
        );

        $(".increase-quantity").click(function () {
          var productId = $(this).data("id");
          $.ajax({
            type: "POST",
            url: "/cart/update",
            data: { product_id: productId, quantity: element.quantity + 1 },
            dataType: "json",
            success: function (response) {
              if (response.status === "success") {
                updateCart();
              } else {
                notyf.error(response.message);
              }
            },
            error: function () {
              notyf.error("Something went wrong");
            },
          });
        });

        $(".decrease-quantity").click(function () {
          var productId = $(this).data("id");
          $.ajax({
            type: "POST",
            url: "/cart/update",
            data: { product_id: productId, quantity: element.quantity - 1 },
            dataType: "json",
            success: function (response) {
              if (response.status === "success") {
                updateCart();
              } else {
                notyf.error(response.message);
              }
            },
            error: function () {
              notyf.error("Something went wrong");
            },
          });
        });

        $(".delete-item").click(function () {
          var productId = $(this).data("id");
          $.ajax({
            type: "POST",
            url: "/cart/delete",
            data: { product_id: productId },
            dataType: "json",
            success: function (response) {
              if (response.status === "success") {
                updateCart();
              } else {
                notyf.error(response.message);
              }
            },
            error: function () {
              notyf.error("Something went wrong");
            },
          });
        });
      });
    },
  });
}
updateCart();

var notyf = new Notyf({ duration: 3000 });

$("#addToCart").click(function (e) {
  e.preventDefault();

  var urlParams = new URLSearchParams(window.location.search);
  var paramValue = urlParams.get("variant");
  $("#addToCart").text("Adding...");
  $.ajax({
    type: "POST",
    url: "/cart/add",
    data: { product_id: paramValue },
    dataType: "json",
    success: function (response) {
      notyf.success("Added Successfully");
      $("#addToCart").text("Added");
      $("#items").html("");
      updateCart();
    },
    error: function () {
      notyf.error("Something went wrong");
    },
  });
});


$("#shopall").click(function (e) { 
  e.preventDefault();
  $("#shopall-dropdown").toggleClass("show-dropdown");
});

$(document).click(function (e) {
  if (!$(e.target).closest("#shopall, #shopall-dropdown").length) {
    $("#shopall-dropdown").removeClass("show-dropdown");
  }
});



$(".add-to-wishlist").click(function (e) { 
  e.preventDefault();
  var id = $(this).data("id");
  var $this = $(this);
  $.ajax({
    type: "POST",
    url: "/wishlist",
    data: { product_id: id },
    dataType: "json",
    success: function (response) {
      notyf.success(response.message);
      $this.text("Added");
    },
    error: function () {
      notyf.error("Something went wrong");
    },
  });

});