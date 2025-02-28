///////////////////////////////////////////////////// 
/// utility functions
function getNumber(str) {
    // Regular expression to match the final digits
    let regex = /(\d+)$/;
    // Apply the regex to extract the digits at the end of the string
    let match = str.match(regex);
    // If a match is found, return the number, otherwise return null
    return match ? match[0] : null;
};

/// Global variables
const animations = Array.from(document.querySelectorAll('.animation'));
let animation_state = new Array(animations.length).fill(false);
let animation_on_stage = null;
let index0;
let position;
let viewportWidth;
let scale;

/////////////////////////////////////////////////////
// Intersection Observer options
const options = {
    root: null, // Use the viewport as the root
    rootMargin: '0px', // No margin around the root
    threshold: 0.1 // Trigger when at least 10% of the target is visible
};

// Callback function for the Intersection Observer
const callback = (entries, observer) => {
entries.forEach((entry) => {
    let index = animations.findIndex(item => item.id === entry.target.id);
    if (entry.isIntersecting) {
            // new animation
            index0 = animation_state.findIndex(item => item === true);
            if (index0 == -1){
                    // set new
                    animation_on_stage = animations[index];
                    animation_on_stage.classList.remove('off_stage');
                    animation_on_stage.classList.add('on_stage');
                    console.log(animation_on_stage.id);
                    
                    // Ensure backgrounds are visible
                    const backgrounds = animation_on_stage.querySelectorAll('.back');
                    backgrounds.forEach(bg => {
                        bg.style.visibility = 'visible';
                    });
                    
                    // Calculate initial position
                    setScroll();
            }
            else{
                    if(index0 > index){
                            // remove old
                            animation_on_stage = null;
                            animations[index0].classList.remove('on_stage');
                            animations[index0].classList.add('off_stage');
                            // set new
                            animation_on_stage = animations[index];
                            animation_on_stage.classList.remove('off_stage');
                            animation_on_stage.classList.add('on_stage');
                            console.log(animation_on_stage.id);
                            
                            // Ensure backgrounds are visible
                            const backgrounds = animation_on_stage.querySelectorAll('.back');
                            backgrounds.forEach(bg => {
                                bg.style.visibility = 'visible';
                            });
                            
                            // Calculate initial position
                            setScroll();
                    }
            };
            animation_state[index]=true;
    } else {
            // animation not in viewport
            if(animation_state[index]){
                    // remove old
                    if(animation_on_stage != null){
                            if(animation_on_stage.id === entry.target.id){
                                    animation_on_stage = null;
                                    animations[index].classList.remove('on_stage');
                                    animations[index].classList.add('off_stage');
                            }
                    }
                    animation_state[index]=false;
            }
    }
});
};

const observer = new IntersectionObserver(callback, options);

// Observe each animation element
document.querySelectorAll('.animation').forEach(anima => {
    observer.observe(anima);
});

// scroll value
const setScroll = () => {
const rect = animation_on_stage.getBoundingClientRect();

// Original calculation with a small adjustment to make backgrounds appear below HTML elements
// The offset ensures the background starts at the bottom of the viewport when the animation enters
position = (-rect.top+window.innerHeight)/(+rect.bottom-rect.top+window.innerHeight)*100;

// Add a small offset to make the background start at the bottom of the viewport
// This ensures it appears below the HTML elements
position = Math.max(0, position - 5);  // 5% offset can be adjusted

if (position<0){ position = 0;}
if (position>100){ position = 100;}

console.log(animation_on_stage.id+'>>> '+position);
id = getNumber(animation_on_stage.id);
document.body.style.setProperty('--scroll_'+id, position);
};
// listener         
window.addEventListener('scroll', () => {
//console.log(window.pageYOffset / (document.body.offsetHeight - window.innerHeight));
if (animation_on_stage != null){
    setScroll();
    
    // Ensure backgrounds remain visible during scrolling
    const backgrounds = animation_on_stage.querySelectorAll('.back');
    backgrounds.forEach(bg => {
        bg.style.visibility = 'visible';
    });
}
}, false);

// listeners for resize
const handleResize = () => {
  // Get the current viewport width
  viewportWidth = window.innerWidth;
  
  // Get the reference width from the first back element of the current animation
  let referenceWidth = 1079; // Default fallback value
  
  // If there's an animation on stage, get the width from its first back element
  if (animation_on_stage) {
    const firstBack = animation_on_stage.querySelector('.back');
    if (firstBack) {
      // Get the computed width or the width from the style
      const computedStyle = window.getComputedStyle(firstBack);
      const width = parseInt(computedStyle.width, 10);
      if (!isNaN(width) && width > 0) {
        referenceWidth = width;
      }
    }
  } else {
    // If no animation is on stage yet, try to get width from any .back element
    const anyBack = document.querySelector('.back');
    if (anyBack) {
      const computedStyle = window.getComputedStyle(anyBack);
      const width = parseInt(computedStyle.width, 10);
      if (!isNaN(width) && width > 0) {
        referenceWidth = width;
      }
    }
  }
  
  // Calculate the scale based on the viewport width and reference width
  scale = viewportWidth / referenceWidth;
  
  // Apply the scale to the CSS variable
  document.documentElement.style.setProperty('--scale', scale);
  
  // Update other viewport-dependent variables
  document.documentElement.style.setProperty('--vw', `${viewportWidth}px`);
  document.documentElement.style.setProperty('--vh', `${window.innerHeight}px`);
  
  // Log the scale for debugging
  console.log(`Viewport width: ${viewportWidth}px, Reference width: ${referenceWidth}px, Scale: ${scale}`);
};

// Call handleResize immediately to set initial scale
handleResize();

window.addEventListener('load', handleResize);
window.addEventListener('resize', handleResize);