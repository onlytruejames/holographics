# holographics

Here's the documentation for how to use holographics, and how to design your own effects.

## Using

### Projects

Projects are located in the `projects` directory in their own directories. Here's the recommended format of a `projects` directory:
```fs
projects/
    myProject/
        project.json
        media/
            example.png
            animated.gif
```
#### project.json
`project.json` is a JSON file describing the sequence of effects and the metadata of a project. It is required. Here's an example file from the project "testProject":

```json
{
	"name": "testProject",
    "scale": 1,
	"sequence": [
        [
    		{
    			"effectName": "camera",
    			"effectVariables": {
    				"Preserve Aspect Ratio": true
                }
			}, {
				"effectName": "blur",
				"effectVariables": {
					"Amount": 10
				}
			}, {
    			"effectName": "sine",
				"effectVariables": {
					"Multiplier": 0.1
				},
                "compositeMode": "replace"
			}
		]
    ]
}
```
Lines 2-4 describe the metadata of the project.

|**Name**|**Description**|**Optional**
|-|-|-
|name|The name of the project|No
|scale|Images are resized to 1/scale of their width and height|Yes
|sequence|The list of effects used in the project at any point|No

The sequence is an array of other arrays. These smaller arrays are called Slides, which describe all the effects on screen at a given time.

Slides are arrays of data describing Effects. These are shown on lines 6-22.

The format of an effect is:
```json
{
	"effectName": "fadeback",
	"compositeMode": "replace",
	"effectVariables": {
		"Rate": 1,
		"Mode": 2,
		"Reducing gap": 1
	}
}
```
|**Name**|**Purpose**|**Required**|**Default value**
|-|-|-|-
|effectName|Specify the name of the effect|Yes|N/A
|compositeMode|Determines how the result of this effect is combined with the result of the previous effect|No|replace
|effectVariables|Specify the name of the effect|Depends|See variable reference table

|**effectName**|**Description**
|-|-
|blur|Blurs an image
|camera|Returns a photo from a webcam
|difference|Compares two frames and returns the difference in RGB values
|expandingColours|A dissolving effect where bright colours spread out
|faceOnly|Removes everything that's not a face
|fadeback|Pastes the previous frame behind the current frame, slightly smaller
|fadeVelocity|Same as before but instead offsets the previous frame instead of making it smaller
|greenScreen|Sets everything close to a given colour to be transparent
|invert|Inverts the image
|mediaLoader|Returns an image (animated or not) from a designated image file, relative to `holographics/`
|pixelDifference|Returns the RGB difference between a pixel and its neighbours
|randomColourRemover|Removes/preserves a random colour in the image.
|santa|Adds a santa face to everything it sees
|saturate|Saturates the image
|sine|Returns the sine of an image
|slideInception|Simulate a slide within an effect
|strobe|Change the brightness of the image quickly

#### media/
`media/` is not required, but is recommended to improve compatibility with editing software which may be developed in the future. This directory should contain all the relevant media in a project.