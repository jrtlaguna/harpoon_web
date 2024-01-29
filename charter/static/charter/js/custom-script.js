$(document).ready(function () {
  // $( '.datepicker' ).datepicker();
  // $(function () {
  //   $(".datepicker").datepicker()
  //   $(".timepicker").datetimepicker({
  //     format: "HH:mm",
  //   })
  // })

  function init_digit_group() {
    $(".digit-group")
      .find("input")
      .each(function () {
        $(this).attr("maxlength", 1)
        $(this).on("keyup", function (e) {
          var parent = $($(this).parent())

          if (e.keyCode === 8 || e.keyCode === 37) {
            var prev = parent.find("input#" + $(this).data("previous"))

            if (prev.length) {
              $(prev).select()
            }
          } else if (
            (e.keyCode >= 48 && e.keyCode <= 57) ||
            (e.keyCode >= 65 && e.keyCode <= 90) ||
            (e.keyCode >= 96 && e.keyCode <= 105) ||
            e.keyCode === 39
          ) {
            var next = parent.find("input#" + $(this).data("next"))

            if (next.length) {
              $(next).select()
            } else {
              if (parent.data("autosubmit")) {
                parent.submit()
              }
            }
          }
        })
      })
  }

  function init_stick() {
    var stick_nav_offset_top = $(".site-header")
    if (stick_nav_offset_top?.offset()?.top) {
      stick_nav_offset_top = stick_nav_offset_top.offset().top
      if (stick_nav_offset_top) {
        var stick_nav = function () {
          var scrollTop = $(window).scrollTop()
          if (scrollTop > stick_nav_offset_top) {
            $(".site-header").addClass("stick")
          } else {
            $(".site-header").removeClass("stick")
          }
        }
        stick_nav()
        $(window).scroll(function () {
          stick_nav()
        })
      }
    }
  }

  function init_password() {
    $(`input[type=password]`).after(`
          <div class="show_pass-container">
              <a href="javascript:void(0)" class="show_pass-label" > <i class="far fa-eye txt-color-black" > </i></a>
            </div>
      `)

    $(`input[type=password]`).parent().addClass("password-content")
  }
  init_password()
  init_digit_group()
  init_stick()
})
// SHOW PASSWORD

$(document).on("click", ".show_pass", function () {})

$(document).on("click", ".show_pass-label", function () {
  if ($(this).hasClass("pass-show")) {
    $(this)
      .closest(`.show_pass-container`)
      .find(".show_pass-label")
      .html("<i class='far fa-eye txt-color-black'></i> ")
    $(this)
      .closest(`.password-content`)
      .find(`input[type=text]`)
      .attr("type", "password")
    $(this).removeClass("pass-show")
  } else {
    $(this)
      .closest(`.show_pass-container`)
      .find(".show_pass-label")
      .html(
        "<i class='far fa-eye-slash txt-color-black' style='opacity:0.5'></i> "
      )
    $(this)
      .closest(`.password-content`)
      .find(`input[type=password]`)
      .attr("type", "text")
    $(this).addClass("pass-show")
  }
})

$(document).on("click", ".cuisine-cbx", function () {
  if ($(this).is(":checked")) {
    $(this).parent(".cuisine").find(".cuisine-note").addClass("show")
  } else {
    $(this).parent(".cuisine").find(".cuisine-note").removeClass("show")
  }
})

$(document).on("click", ".cuisine-cbx-sub", function () {
  if ($(this).is(":checked")) {
    $(this).parent(".cuisine-sub").find(".cuisine-note-sub").addClass("show")
  } else {
    $(this).parent(".cuisine-sub").find(".cuisine-note-sub").removeClass("show")
  }
})

$(document).on("click", "#add_bev", function () {
  $i = $i = $(this).closest(".inc").find("#ind_bev").val()
  $i++

  $(this).closest(".inc").find("#ind_bev").val($i)
})

$(document).on("click", "#minus_bev", function () {
  $i = $i = $(this).closest(".inc").find("#ind_bev").val()
  $i--

  $(this).closest(".inc").find("#ind_bev").val($i)

  if ($i <= 0) {
    $i = $(this).closest(".inc").find("#ind_bev").val(0)
  }
})

//
$(document).on("click", ".cuisine-cbx-sub-sub", function () {
  if ($(this).is(":checked")) {
    $(this)
      .parent(".cuisine-sub-sub")
      .find(".cuisine-note-sub-sub")
      .addClass("show")
  } else {
    $(this)
      .parent(".cuisine-sub-sub")
      .find(".cuisine-note-sub-sub")
      .removeClass("show")
  }
})
