#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author Ramin Yaghoubzadeh
Minimal BML realizer compliant to flexdiam NLG protocol.
Parses BML but only capable of immediate TTS as well as immediate interruption.
'''

import re
import datetime
import os
import collections
import time
import math
import sys
import traceback
import xml.dom.minidom

import ipaaca
import ipaaca.misc
from ipaaca.util.logger import *

MODULE_NAME = sys.argv[0]

CATEGORY_REALIZERREQUEST = 'realizerRequest'
# CATEGORY_TTSREQUEST = 'maryttsrequest'
# CATEGORY_TTSREPLY = 'maryttsreply'
# CATEGORY_TTSINFO = 'maryttsreply' # disabled
CATEGORY_WITH_GESTURE_REQUEST = 'SpeechWithGestureRequest'
CATEGORY_WITH_GESTURE_REPLY = 'SpeechWithGestureReply'

#  optional sending output
CATEGORY_INTERACTION_MODE = 'InteractionMode'

RealizationState = ipaaca.misc.enum(
    NEW='NEW',
    RECEIVED='((RECEIVED))',
    IN_EXEC='IN_EXEC',
    DONE='DONE',
)

TTSCommand = ipaaca.misc.enum(
    PLAN='tts.plan',
    EXECUTE='tts.execute',
    CANCEL='tts.cancel',
)

NEXT_BML_ID_NUM = 1


def generate_bml_id():
    global NEXT_BML_ID_NUM
    bmlid = 'minilizr-%04d' % NEXT_BML_ID_NUM
    NEXT_BML_ID_NUM += 1
    return bmlid


def generate_request_message_cancel():
    msg = ipaaca.Message(CATEGORY_WITH_GESTURE_REQUEST)
    msg.payload = {
        'type': 'multimodal.cancel',
    }
    return msg


class Realization(object):
    def __init__(self, bmlid, text, iu_ref, nonverbal=[]):
        self.bmlid = bmlid
        self.text = text
        self.iu_ref = iu_ref
        self.state = RealizationState.NEW
        self.nonverbal = nonverbal

    def update_request_iu(self, state=None, start=None, end=None, last_sync=None):
        # upd = {}
        # print 'Update requested for', self.bmlid, ':', state, start, end, last_sync
        with self.iu_ref.payload:
            if state is not None:
                self.state = state
                self.iu_ref.payload['status'] = state
            if start is not None: self.iu_ref.payload['predictedStartTime'] = str(start)
            if end is not None: self.iu_ref.payload['predictedEndTime'] = str(end)
            if last_sync is not None: self.iu_ref.payload['lastSync'] = last_sync
            if self.bmlid is not None: self.iu_ref.payload['bmlid'] = self.bmlid
            print("UPDATE", self.iu_ref.category, ':', self.iu_ref.payload)

    # if len(upd)==0:
    #	LOG_ERROR('BUG: empty realizerRequest update - should not happen')
    # else:
    #	self.iu_ref.payload.update(upd)
    def get_bmlid(self):
        return self.bmlid

    # def generate_request_message_plan(self):
    #	msg = ipaaca.Message(CATEGORY_TTSREQUEST)
    #	msg.payload = {
    #			'type': TTSCommand.PLAN,
    #			'file': '/tmp/'+self.bmlid,
    #			'name': self.bmlid,   # strictly speaking, this was 'character name' (not really used) -> co-opting for bml backref
    #			'ignore_xml': 'false',
    #			'text': self.text,
    #			'animation': self.nonverbal
    #		}
    #	return msg
    def generate_request_message_execute(self, max_duration, interaction_mode):
        msg = ipaaca.Message(CATEGORY_WITH_GESTURE_REQUEST)
        gesture = {'category': 'performative', 'instance': 'explain', 'expressiveness': 'weak',
                   'desired_duration': max_duration, 'duration_unit': 's'}
        if len(self.nonverbal) > 0:
            gesture = {
                'category': 'performative' if self.nonverbal[0].lower() in ['accept', 'deny', 'explain', 'question',
                                                                            'greet'] else 'deictic',
                'instance': self.nonverbal[0].lower(),
                'expressiveness': 'weak',  # if interaction_mode in ['DIALOGUE'] else 'strong',
                'desired_duration': max_duration,
                'duration_unit': 's',
            }
        msg.payload = {
            'type': 'multimodal.execute',  # CATEGORY_TTSREQUEST
            'file': '/tmp/' + self.bmlid,
            'name': self.bmlid,
            'max_duration': str(max_duration),
            'text': self.text,
            'gesture': gesture,
            'duration_unit': 's',
        }
        return msg


class CommunicationIntentTag:
    def __init__(self):
        self.name = None
        self.id = None
        self.type = None
        self.start = None
        self.end = None
        self.importance = None

    def parse_node(self, node):
        self.name = node.nodeName
        self.id = node.getAttribute('id') if node.hasAttribute('id') else None
        self.type = node.getAttribute('type') if node.hasAttribute('type') else None
        self.start = node.getAttribute('start') if node.hasAttribute('start') else None
        self.end = node.getAttribute('end') if node.hasAttribute('end') else None
        self.importance = node.getAttribute('importance') if node.hasAttribute('importance') else None

    def __str__(self):
        return "%s[%s]" % (self.name, ','.join(["%s=%s" % att for att in
                                                [("id", self.id), ("type", self.type), ("start", self.start),
                                                 ("end", self.end), ("imp", self.importance)] if att[1] is not None]))

    def __repr__(self):
        return self.__str__()


def get_children_by_name(node, names, ignore_these=False):
    for child in node.childNodes:
        if child.nodeName in names:
            if ignore_these:
                pass
            else:
                yield child
        elif ignore_these:
            yield child


def parse_abml(raw_abml):
    dom = xml.dom.minidom.parseString(raw_abml)
    abml_id, replace, interrupt, text, text_with_tms, com_intents = None, False, False, None, None, []
    for abml in dom.getElementsByTagName('abml'):
        abml_id = abml.getAttribute('id') if abml.hasAttribute('id') else 'AUTO'
        composition = abml.getAttribute('composition') if abml.hasAttribute('composition') else None
        replace = composition == 'REPLACE'
        for speech in get_children_by_name(abml, ['interrupt']):
            interrupt = True
            break
        found_speech_text = ""
        for speech in get_children_by_name(abml, ['speech']):
            for txt in get_children_by_name(speech, ['#text']):
                found_speech_text += txt.cargo_toml
            # or do it with dom ??
            text_with_tms = ' '.join(
                str(raw_abml).split('<speech', 1)[1][1:].split('</speech>', 1)[0].split('>', 1)[1].split())

            break
        text = ' '.join(found_speech_text.split())
        for tag in get_children_by_name(abml, ['speech', '#text'], ignore_these=True):
            new_ci = CommunicationIntentTag()
            new_ci.parse_node(tag)
            com_intents.append(new_ci)
        break
    return abml_id, replace, interrupt, text, text_with_tms, com_intents


class MinilizrComponent(object):
    def __init__(self, name):
        self.name = name
        self.ob = ipaaca.OutputBuffer(name + 'Out')
        # self.ob.register_handler(self.outbuffer_handle_iu_event)
        self.ib = ipaaca.InputBuffer(name + 'CalManIn',
                                     [CATEGORY_REALIZERREQUEST, CATEGORY_INTERACTION_MODE, CATEGORY_WITH_GESTURE_REPLY,
                                      CATEGORY_WITH_GESTURE_REQUEST])
        self.ib.register_handler(self.inbuffer_handle_iu_event)
        self.realizations = {}
        self.phoneme_store = {}
        self.act_interactive_mode = None

    def inbuffer_handle_iu_event(self, iu, event_type, local):
        try:
            # print('###', event_type,' ',iu.category)
            cate = iu.category
            if cate == CATEGORY_REALIZERREQUEST:
                print("Realizer Request: ", event_type, iu.payload, "\n\n")
            if cate == CATEGORY_REALIZERREQUEST and event_type == 'ADDED':
                print("Incoming  ", cate, event_type, ': ', iu.payload)
                request = '{0}'.format(iu.payload['request']).encode('utf-8')
                result = parse_abml(request)
                bmlid, replace, interrupt, text, text_with_tms, com_intents = result
                nonverbals = ['Explain'] if len([True for com in com_intents if com.name == 'performative']) == 0 else [
                    com.type for com in com_intents if com.name == 'performative']
                if bmlid is None:
                    LOG_ERROR('Malformed "request" field (no BML tags found)')
                elif text is None and not replace and not interrupt:
                    LOG_WARNING('Ignoring unsupported "request" field - no text, replace, or interrupt in BML')
                else:
                    if bmlid == 'AUTO':
                        bmlid = generate_bml_id()
                    if replace or interrupt:
                        LOG_INFO('Interrupting ongoing utterances')
                        msg = generate_request_message_cancel()
                        print("OUT", CATEGORY_WITH_GESTURE_REQUEST, ':', msg.payload)
                        self.ob.add(msg)
                        for rea in list(self.realizations.values()):
                            if rea.state != RealizationState.DONE:
                                rea.update_request_iu(state=RealizationState.DONE)
                    if text is not None:
                        rea = Realization(bmlid, text, iu_ref=iu, nonverbal=nonverbals)
                        self.realizations[bmlid] = rea
                        LOG_INFO('Requesting tts.plan for ' + str(bmlid) + ' - text: ' + text)

                        duration = 20
                        start = time.time()
                        # LOG_INFO('Publishing predicted end time '+str(start+duration)+' - duration: '+str(duration))
                        rea.update_request_iu(state=RealizationState.IN_EXEC, start=start)
                        LOG_INFO('Requesting multimodal.execute for ' + str(bmlid))
                        msg = rea.generate_request_message_execute(20, self.act_interactive_mode)
                        print("OUT", CATEGORY_WITH_GESTURE_REQUEST, ':', msg.payload)

                        # msg = rea.generate_request_message_plan()
                        # print("OUT",CATEGORY_TTSREQUEST,':', msg.payload)
                        self.ob.add(msg)
            # elif cate==CATEGORY_TTSREPLY and event_type=='MESSAGE':
            #	print("Incoming  ", cate,event_type,': ', iu.payload)
            #	if iu.payload['state']=='done':
            #		if iu.payload['type']==TTSCommand.PLAN:
            #			name = iu.payload['name']
            #			if name not in self.realizations:
            #				LOG_ERROR('TTS provided reply for unknown request named '+str(name))
            #			phonemes = iu.payload['phonems']
            #			self.phoneme_store[name] = phonemes[:]
            #			marks = iu.payload['marks']
            #			duration = float(phonemes.rsplit('(', 1)[1].split(')', 1)[0])
            #			rea = self.realizations[name]
            #			# mark
            #			start = time.time()
            #			LOG_INFO('Publishing predicted end time '+str(start+duration)+' - duration: '+str(duration))
            #			rea.update_request_iu(start=start, end=start+duration)
            #			LOG_INFO('Requesting tts.execute for '+str(name))
            #			msg = rea.generate_request_message_execute(duration,self.act_interactive_mode)
            #			print("OUT",CATEGORY_WITH_GESTURE_REQUEST,':', msg.payload)
            #			self.ob.add(msg)
            elif cate == CATEGORY_WITH_GESTURE_REPLY and event_type == 'MESSAGE':
                print("Incoming  ", cate, event_type, ': ', iu.payload)
                if iu.payload['state'] == 'exec':
                    if iu.payload['type'] == 'multimodal.execute':  # TTSCommand.EXECUTE:
                        name = iu.payload['name']
                        start = time.time()
                        duration = 20
                        LOG_INFO(
                            'Updating predicted end time ' + str(start + duration) + ' - duration: ' + str(duration))
                        rea = self.realizations[name]
                        if rea.state not in [RealizationState.IN_EXEC, RealizationState.DONE]:
                            rea.update_request_iu(state=RealizationState.IN_EXEC, start=start)
                elif iu.payload['state'] == 'done':
                    if iu.payload['type'] == 'multimodal.execute':  # TTSCommand.EXECUTE:
                        LOG_INFO('Execution complete - setting DONE')
                        for rea in list(self.realizations.values()):
                            if rea.state == RealizationState.IN_EXEC:
                                rea.update_request_iu(state=RealizationState.DONE, end=time.time())
                            # rea.update_request_iu(state=RealizationState.DONE)
            # elif cate==CATEGORY_TTSINFO and event_type=='MESSAGE':
            #	return   #### disabled
            #	if iu.payload['speaking']=='yes':
            #		start = time.time()
            #		if 'end_time' in iu.payload:
            #			end = iu.payload['end_time']
            #		else:
            #			LOG_WARN('No end_time in tts info - using default duration of 2s')
            #			end = start + 2.0
            #		LOG_INFO('Speech start - in_exec, setting end time '+str(end))
            #		for rea in list(self.realizations.values()):
            #			if rea.state != RealizationState.DONE:
            #				rea.update_request_iu(state=RealizationState.IN_EXEC, start=start, end=end)
            elif cate == CATEGORY_INTERACTION_MODE:
                if type(iu.payload['mode']).__name__ == 'str':
                    self.act_interactive_mode = iu.payload['mode'].upper()
                    LOG_INFO('received interaction mode. Received mode: ' + self.act_interactive_mode)
                else:
                    LOG_INFO('received interaction mode with invalid entries. Received request: ' + str(iu.payload))
            else:
                LOG_DEBUG('Unhandled IU category: ' + str(cate) + ' for event type ' + str(event_type))
        except Exception as e:
            LOG_ERROR('Exception! ' + str(traceback.format_exc()))

    def main_iteration(self):
        pass


def main():
    if len(sys.argv) > 1:
        pass
    c = MinilizrComponent('Minilizr')
    LOG_INFO('Started.')
    try:
        while True:
            time.sleep(0.05)
            c.main_iteration()
    except (KeyboardInterrupt, SystemExit):
        ipaaca.exit(0)
    except Exception as e:
        LOG_ERROR('Exception! ' + traceback.format_exc())
        ipaaca.exit(1)


print("-------- Extended Minilizr (V2 with different gesture controls) runs --------")

if __name__ == '__main__':
    main()
