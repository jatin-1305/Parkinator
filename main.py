import database as db
import databaseVisitor as visitor_db
import random
import smtplib
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty,ObjectProperty

Window.size=(470,600)

class IdPopup(Popup):
    pass
class CheckoutPopup(Popup):
    pass
class VisitorSelectWindow(Screen):
    pass
class VisitorCheckoutWindow(Screen):
    def visitor_checkout(self):
        mobile_number = self.ids.visitor_mobile.text
        visitor_db.fb_visitor_checkout(mobile_number)
        CheckoutPopup().open()

class FirstWindow(Screen):
    pass
class SecondWindow(Screen):
    def facid(self):
        return fid

    def fcheck(self):
        try:
            global fid
            fid = self.ids.fid.text
            fid=fid.upper()
            fpass = self.ids.fpass.text
            status = db.person_type_func(fid)
            em = status
            if (em == "Faculty"):
                if(db.fb_check(fid,fpass)):
                        return True
            return False
        except:
            pass

class ThirdWindow(Screen):
    def checkbox_click(self,instance,value,t):
        global vehicle_type
        if value== True:
            self.ids.ll.text='You have selected '+t
            if t == '2-wheeler':
                vehicle_type=2
            elif t=='4-wheeler':
                vehicle_type=4
        elif value== False:
            self.ids.ll.text=''
    def vis(self):
        try:
            mobile_number=self.ids.mobile_number.text
            name_v=self.ids.name_v.text
            if(len(mobile_number) != 10):
                popup = Popup(title='Error', content=Label(text='Mobile no. should be\nof 10 digits'), size_hint=(0.5, 0.4),
                              auto_dismiss=True)
                popup.open()
                self.manager.current = 'Third'

            elif(name_v != '' and mobile_number != ''):
                a=visitor_db.fb_insert_visitor_data(mobile_number,name_v,vehicle_type)
                popup2 = Popup(title='Slot Number', content=Label(text='Your slot is '+a),size_hint= (0.5,0.4),
                                      auto_dismiss=True)
                popup2.open()
                self.manager.current = 'First'
            elif(name_v=='' or mobile_number==''):
                popup = Popup(title='Error', content=Label(text='Enter all details'), size_hint=(0.5, 0.4),
                              auto_dismiss=True)
                popup.open()
                self.manager.current = 'Third'
        except:
            pass
class SlotWindow(Screen):
    pass
class StudentWindow(Screen):
    def stuid(self):
            return sid

    def scheck(self):
        try:
            global sid
            sid = self.ids.sid.text
            sid=sid.upper()
            StudentWindow.stuid(self)
            spass = self.ids.spass.text
            status = db.person_type_func(sid)
            em = status
            if (em == "Student"):
                if ( db.fb_check(sid, spass)):
                    return True
            return False
        except:
            return False
            pass

class EnterWindow(Screen):
    pass
class UidWindow(Screen):
    def delete_data(self):
        try:
            uid = self.ids.uid.text
            uid=uid.upper()
            db.fb_delete(uid)
            AllPopup().open()
        except:
            pass
class AdminWindow(Screen):
    def aaa(self):
        uid = self.ids.uid.text
        passs = self.ids.passs.text
        if uid=='admin123' and passs=='pass123':
            self.ids.uid.text=''
            self.ids.passs.text=''
            return True
    def aaaa(self):
        self.ids.uid.text=''
        self.ids.passs.text=''
        self.ids.lab.text='(Wrong ID or Password!)'

class AddWindow(Screen):
    val=None
    def spinner_clicked(self,value):
        global val
        self.ids.spinner_id.text= value
        if value=='Student':
            val=0
        elif value=='Faculty':
            val=1
    def nadd_check(self):
        nname = self.ids.nname.text
        npass = self.ids.npass.text
        nid = self.ids.nid.text
        nemail = self.ids.nemail.text
        nid=nid.upper()
        db.fb_insert_member_data(nid,npass,nname,nemail,val)

    def validation(self):
        nname = self.ids.nname.text
        npass = self.ids.npass.text
        count,c1 = 0,0
        special = "[@_!#$%^&*()<>?/\|}{~:]"
        for i in nname:
            if i.isnumeric() or i in special:
                c1+=1
        if c1==0:
            if len(npass) >= 6:
                count += 1

            for i in npass:
                if i in special:
                    count += 1
                    break
            for i in npass:
                if i.isupper():
                    count += 1
                    break
            for i in npass:
                if i.isnumeric():
                    count += 1
                    break
        if count == 4 and c1==0:
            count = 0
            AddWindow.nadd_check(self)
            popup1 = Popup(title='DONE', content=Label(text='Data Added Successfully'), size_hint=(0.5, 0.4),
                          auto_dismiss=True)
            popup1.open()
            self.ids.nname.text = ''
            self.ids.npass.text = ''
            self.ids.nid.text = ''
            self.ids.nemail.text = ''
            return True
        else:
            c1=0
            count=0
            return False

class FourthWindow(Screen,Widget):

    def gets(self):
        self.ids.vname.text=name
        self.ids.vid.text = id
        self.ids.vpass.text = passs
        self.ids.vslot.text = slot
        self.ids.vemail.text = email
        self.ids.vvehicle_type.text = str(vehicle_type)
        self.ids.vperson_type.text = person_type

    def printing(self,name, id, passs, slot, email, vehicle_type, person_type):
        pass

class Uid1Window(Screen):
    def view_data(self):
        uid=self.ids.uid.text
        uid=uid.upper()
        try:
            l=db.fb_get_details(uid)
            global name
            global id
            global passs
            global slot
            global email
            global vehicle_type
            global person_type
            name, id, passs, slot, email, vehicle_type, person_type = l.get('name'), uid , l.get('password'), l.get('allotment'), l.get('email'), l.get('vehicle_type'), l.get('person_type')
            if slot=='?':
                slot='Not alloted'
            if vehicle_type==-1:
                vehicle_type='Not Selected'
            if person_type==0:
                person_type='Student'
            elif person_type==1:
                person_type='Faculty'

            FourthWindow().printing(name, id, passs, slot, email, vehicle_type, person_type)
            FourthWindow().gets()
            self.manager.current='Fourth'
        except Exception as e:
            IdPopup().open()
            self.manager.current='Enter'


class Del1Window(Screen):
    def get_otp_id(self):
        return otp_id
    def get_mail(self):
        try:
            global otp_id
            otp_id = self.ids.otp_id.text
            otp_id=otp_id.upper()
            Del1Window.get_otp_id(self)
            email = db.fb_email_OTP(otp_id)
            em=email

            global otp
            otp=random.randint(100000, 999999)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
		#enter your mail password under the ******
            s.login("cse.19bcs3786@gmail.com", "*****")
            message = 'Your OTP for changing password in Parkinator app is ' + str(otp)
            s.sendmail("cse.19bcs3786@gmail.com", em, message)
            s.quit()
        except:
            IdPopup().open()


    def erroropen(self):
        OtpPopup().open()

    def otpcheck(self,otp_number):
        if str(otp)==otp_number:
            return True
        else:
            return False



class OtpPopup(Popup):
    def abc(self):
        a1= False
        otp_number=self.ids.otp_number.text
        a1=Del1Window().otpcheck(otp_number)
        if a1:
            return True
        else:
            return False

class NewWindow(Screen):
    def confirm(self):
        global new1
        new1=self.ids.new1.text
        new2=self.ids.new2.text
        count=0
        sp = "[@_!#$%^&*()<>?/\|}{~:]"
        if new1==new2:
            if len(new1) >= 6:
                count += 1

            for i in new1:
                if i in sp:
                    count += 1
                    break
            for i in new1:
                if i.isupper():
                    count += 1
                    break
            for i in new1:
                if i.isnumeric():
                    count += 1
                    break
        if count==4:
            count=0
            zz=Del1Window().get_otp_id()
            db.fb_update_password(zz, new1)
            return True
        else:
            count=0
            return False



class FcheckinWindow(Screen):
    def ccc1(self):
        global co_id
        co_id=SecondWindow().facid()
        db.fb_checkout(co_id)
        popup1 = Popup(title='DONE', content=Label(text='Checkout Successfully'), size_hint=(0.5, 0.4),
                       auto_dismiss=True)
        popup1.open()
        self.manager.current='First'

class ScheckinWindow(Screen):
    def ccc2(self):
        global co_id
        co_id=StudentWindow().stuid()
        db.fb_checkout(co_id)
        popup1 = Popup(title='DONE', content=Label(text='Checkout Successfully'), size_hint=(0.5, 0.4),
                       auto_dismiss=True)
        popup1.open()
        self.manager.current = 'First'

class FvehicleWindow(Screen):
    def cc1(self):
        global f_id
        f_id = SecondWindow().facid()

    def checkbox_click(self, instance, value, t):
        global f_vehicle_type
        f_vehicle_type = t
    def printdetails(self):
            abc=db.fb_checkin(f_id.upper(), f_vehicle_type)
            popup1 = Popup(title='DONE', content=Label(text=abc), size_hint=(0.5, 0.4),
                           auto_dismiss=True)
            popup1.open()


class SvehicleWindow(Screen):
    def cc2(self):
        global s_id
        s_id=StudentWindow().stuid()

    def checkbox_click(self, instance, value, t):
        global s_vehicle_type
        if value==True:
            s_vehicle_type=t
        elif value==False:
            s_vehicle_type='0'
    def printdetails(self):
            abc=db.fb_checkin(s_id.upper(),s_vehicle_type)
            popup1 = Popup(title='DONE', content=Label(text=abc), size_hint=(0.5, 0.4),
                           auto_dismiss=True)
            popup1.open()

class AllPopup(Popup):
    pass
class WindowManager(ScreenManager):
    pass

build=Builder.load_file('login.kv')

class ParkinatorApp(App):

    def build(self):
        return build
    def exit(self):
        App.get_running_app().stop()
    def check1(self):
        return True

ParkinatorApp().run()
