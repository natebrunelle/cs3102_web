def fresh_lecture():
    return {
        'title': 'TBA',
        'date': 'TBA',
        'reading': 'TBA',
        'keywords': 'TBA',
        'slides': 'None',
        'video': 'None',
        'weblinks': 'None'
          }

def tup2link(tup):
    link = "new Weblink('"
    link += tup[1]
    link += "', '"
    link += tup[0]
    link += "')"
    return link

def sanitize_str(string):
    if type(string) == type(''):
        return string.replace("'", "\\'")
    else:
        return string

def sanitize_lecture(lecture):
    return {k: sanitize_str(v) for k, v in lecture.items()}

def gen_video_link(video_id):
    if video_id != 'None':
        return 'https://uva.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=' + video_id
    return video_id

def gen_slides_pdf(name):
    if name.strip() != 'None':
        return "'http://www.cs.virginia.edu/~njb2b/cs3102/slides/" + name + ".pdf'"
    return "'None'"

def gen_slides_pptx(name):
    if name.strip() != 'None':
        return "'http://www.cs.virginia.edu/~njb2b/cs3102/slides/" + name + ".pptx'"
    return "'None'"

def createlecture(lecture):
    lecture = sanitize_lecture(lecture)
    lecturestr = 'new Lecture(\n' #intro
    lecturestr += "'"+lecture['title'] + "', \n" #title
    lecturestr += "'" + lecture['keywords'] + "', \n" #keywords
    lecturestr += "'" + lecture['date'] + "', \n" #pubdate
    lecturestr += "['" + gen_video_link(lecture['video']) + "', \n" #video
    lecturestr += "'" + gen_video_link(lecture['video']) + "'], \n" #am video
    lecturestr += gen_slides_pdf(lecture['slides']) + ", \n" #pdf
    lecturestr += gen_slides_pptx(lecture['slides']) + ", \n" #pptx
    lecturestr += "'" + lecture['reading'] + "', \n" #readings
    if lecture['weblinks'] != 'None':
        lecturestr += "[\n "
        for tup in lecture['weblinks']:
            lecturestr += tup2link(tup)
            lecturestr += ", "
        lecturestr += "\n]\n"
    else:
        lecturestr += "'None'\n"
    lecturestr += "), \n"
    return lecturestr


hub = open("index.html", 'w')
hubhead = open("hubhead", 'r')
hubtail = open("hubtail", 'r')
lecture_list = open("lecture_list", 'r')

for line in hubhead.readlines():
    hub.write(line)
currlecture = {}
weblinks = []

for line in lecture_list.readlines():
    if line.strip().lower() == 'current':
        break
    if len(line.strip())>0:
        if line.strip() == 'lecture:':
            if len(currlecture) > 0:
                hub.write(createlecture(currlecture))
            currlecture = fresh_lecture()
            weblinks = []
        else:
            stripped = line.strip()
            parsed = line.split(': ')
            if parsed[0].strip() == 'weblink':
                weblinks.append((parsed[1].strip(),''))
                currlecture['weblinks'] = weblinks
            elif parsed[0].strip() == 'url':
                weblinks[-1] = (weblinks[-1][0], parsed[1].strip())
            elif len(parsed) == 2:
                currlecture[parsed[0].strip()] = parsed[1].strip()
hub.write(createlecture(currlecture))

for line in hubtail.readlines():
    hub.write(line)
