#let myname = "ThanhVu Nguyen"
#let mytitle = "Associate Prof. of Computer Science\nProgram Director, MS Software Engineering"
#let mydept = "Department of Computer Science"
#let myschool = "George Mason University"
#let myaddress = "4400 University Dr. Fairfax, VA 22030"
#let myemail = link("mailto:tvn@gmu.edu")[tvn\@gmu.edu]
#let myweb = link("https://roars.dev")[roars.dev]
#let mystudent = "Firstname"
#let mystudentA = "Firstname Lastname"

#set page(margin: 1in)
#set text(size: 10pt)

#let dkgreen = rgb("#2d6a2d")

// Header box
#block(
  stroke: dkgreen + 1pt,
  inset: 10pt,
  width: 100%,
  radius: (top-left: 8pt, top-right: 8pt),
)[
  #grid(
    columns: (0.35fr, 0.65fr),
    image("gmu3.png", height: 1.2in),
    align(right)[
      #text(size: 14pt, weight: "bold")[#myname] \
      #emph(mytitle) \
      #emph(myschool) \
      #myemail #h(0.5em) #myweb
    ]
  )
]


#v(1em)

#text[#datetime.today().display("[month repr:long] [day], [year]")]

#v(0.5em)

To admission committee:

#v(0.5em)

I am writing to _strongly recommend_ #mystudentA ...

#v(1em)
Sincerely,

#align(center)[
#v(0.5em)
#image("signature.png", height: 0.5in)

#myname, Ph.D. \
Nguyen Engineering Building \#4430 \
#myaddress \
]