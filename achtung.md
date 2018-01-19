
Achtung guys!

Quickcompany proudly presents the first ever [reverse image search tool](https://www.quickcompany.in/trademarks/imagesearch) from India for identifying similar visual trademarks. Our results are [scale, position](https://www.quickcompany.in/trademarks/imageresult?file=https://quickcompanytmp.s3.amazonaws.com/tmimage-640d9d7f-50dd-4cf5-b982-a811c96621cd%2FMitsubishi_logo_2.png&lipi=urn%3Ali%3Apage%3Ad_flagship3_pulse_read%3B%2F%2FDryRVMQ2CiU5SPT0xssA%3D%3D) and [background colour](https://www.quickcompany.in/trademarks/imageresult?file=https://quickcompanytmp.s3.amazonaws.com/tmimage-c6a065ad-a95b-4564-b76a-36d09b95feb8%2Fnikewob.jpg&lipi=urn%3Ali%3Apage%3Ad_flagship3_pulse_read%3B%2F%2FDryRVMQ2CiU5SPT0xssA%3D%3D) invariant, an improvement over the WIPO search engine that has set the global benchmark for shape based similarity results.

<br> <br>

Results vary from spell bounding to absolutely rotten depending on the availability of similar logos in the Indian trademark database. Out of the 3.5 million + trademarks in the Indian Trademark database, approximately a million of them are tagged as visual trademarks but about 70 % of them are wordmarks that are tagged wrongly as visual marks. Out of the remaining 300,000 odd images, more than 50 % of them suffer from bad compression artefacts so we are looking at only about a 100,000 + reasonably good images. Nonetheless, we were able to detect many blatant IP violations of popular brands.

<br> <br>


![image](nikezono.png)

<br> <br>

![image](adidas.png)

<br> <br>
When my partner in crime came up with this cunning idea, with all the recent results in deep learning and jazz, I assumed this to be a trivial problem in the sense that I could use Google Vision / Tensorflow models or Amazon Rekognition to convert the trademark / logo images to word vectors and then compute similar images based on some distance metric that fits the problem. Boy was I wrong. You see all these models used Imagenet data for training their networks so they work well with photographs and probably paintings but spectacularly fail when it comes to logos / trademarks / illustrations. Don't believe me ? You can see the kind of rubbish results google reverse image throws for images that are not indexed by google.
<br> <br>
![image](google1.png)
<br> <br>
![image](google2.png)
<br> <br>
To be fair, every now and then, it identifies an image as an illustration and gives good results.
<br> <br>

![image](google3.png)
<br> <br>
Thus began my journey into attacking this problem from the basics. I knew there had to be a solution to this because WIPO (World Intellectual Property Organization) and EUIPO (European Union Intellectual Property Organization ) have visual search engines that give pretty good results. My first thought was modelling this as a Work / Energy problem - quantifying similarity based on the amount of effort needed to stretch one image to fit another using curvillinear coordinate transformations and soon enough I found [this paper](http://slipguru.disi.unige.it/readinggroup/papers_vis/BMP-shape.pdf?lipi=urn%3Ali%3Apage%3Ad_flagship3_pulse_read%3B%2F%2FDryRVMQ2CiU5SPT0xssA%3D%3D) by Belongie and Jitendra Malik (A stalwart in computer vision who 'was' also a notable critic of the effectiveness of neural networks in computer vision) It seemed to work pretty well on smaller datasets but didn't scale well with larger datasets. I experimented for a month or so with contour based techniques and tried some cunning physics inspired schemes but once again, scaling was the issue.

That is when I found this [excellent summary](http://www.ppgia.pucpr.br/~alekoe/AM/2009/private/veltkamp99stateart.pdf?lipi=urn%3Ali%3Apage%3Ad_flagship3_pulse_read%3B%2F%2FDryRVMQ2CiU5SPT0xssA%3D%3D) of all of the state-of-the-art techniques for shape matching by Professor Veltkamp that guided me for the next 4 months. After exploring every possible technique available in literature and some other, I managed to come up with a mishmash of contour, histogram, moments and hull techniques to come up with these results. There will be more updates in the next couple of weeks. Work is already underway to throw in deep learning to the mix with the right set of data.

<br> <br>
![image](telugu.png)
<br> <br>
![image](logosan0.png)
<br> <br>
![image](logosan1.png)
<br> <br>
![image](logosan.png)
<br> <br>
![image](logosan3.png)
