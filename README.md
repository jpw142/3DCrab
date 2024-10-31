Jack Weber 
CS480
Assignment 2

I found a picture of a crab that I liked and I decided I wanted to recreate that.
First I changed the transformation line to correctly apply all transformations in appropriate order.
I color picked all of the colors I would need from the crab and create my own Color Type for them.
I then created a crab with different shapes from the interface and chaining them together in a proper hierarchy. I also put them in the component list and component dict whenever I added one. I also made sure it to limit the angles for every single limb to ensure the least amount of self intersection possible. I also had difficulty with this but throughout this entire process I had to ensure the left and right sides were mirrored with caused unending issues but I achieved in the end.
I then altered all of the single select functions to work as multi select functions. This mostly consisted of changing the active object index and turning it into a list called active and then just iterating through that list and performing the single select operations on every item in that list; Ensuring to keep active up to date depending on the limbs selected. Having the component dictionary and component list was very useful for this part because it allowed me to reference the components by their names and look up their indexes fairly easily.
I then added a pose selector and pose variable that cycles through all of the poses that I made. In order to make the poses I made a list as long as the number of limbs I had and made each entry correspond to the angle movement that I want that limb to do for that pose. I then iterated through the limbs for each pose and set them to their corresponding angles.	
