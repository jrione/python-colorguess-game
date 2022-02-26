import tkinter as tk, random, requests
from tkinter.messagebox import askyesno
from datetime import date


class Game():
	def __init__(self):
		self.main_frame = tk.Tk()
		self.main_frame.geometry("400x220")
		self.main_frame.minsize(400,220)
		self.main_frame.maxsize(400,220)
		self.main_frame.title("Colortype")

		self.HOSTNAME = 'http://localhost:2390/'
		self.warna = ['Red','Blue','Green','Pink','Black','Yellow','Orange','White','Purple','Brown']
		self.skor = 0
		self.durasi = 3

		self.GUI()

		self.main_frame.mainloop()

	def GUI(self):
		self.instruksi_label = tk.Label(self.main_frame,text='Ketikkan nama warna pada huruf!',font=('Helvetica', 12))
		self.durasi_label = tk.Label(self.main_frame,text="Durasi: "+str(self.durasi), font = ('Helvetica', 12))
		self.skor_label = tk.Label(self.main_frame, text = "Tekan enter untuk memulai",font = ('Helvetica', 12))
		self.warna_label = tk.Label(self.main_frame, font = ('Helvetica', 60))

		self.instruksi_label.pack()
		self.durasi_label.pack()
		self.skor_label.pack()
		self.warna_label.pack()

		self.input = tk.Entry(self.main_frame)
		self.main_frame.bind('<Return>',self.start)
		self.input.pack()
		self.input.focus_set()

		self.lb = tk.Button(self.main_frame,command=self.showLeaderboard,text='Leaderboard')
		self.lb.place(x=300,y=180)

	def start(self,event):
		if self.durasi == 3:
			self.countdown()
		self.nextColor()

	def countdown(self):
		if self.durasi > 0:
			self.durasi -= 1
			self.durasi_label.config(text="Durasi: "+ str(self.durasi))	
			self.durasi_label.after(1000, self.countdown)
		else:
			self.instruksi_label.pack_forget()
			self.durasi_label.pack_forget()
			self.skor_label.pack_forget()
			self.warna_label.pack_forget()
			self.input.pack_forget()

			pujian = ""
			if self.skor > 0:
				if self.skor >= 20:
					pujian = "Hebat!"
				elif self.skor >= 10:
					pujian = "Mantap!"
				elif self.skor < 10:
					pujian = ""
			else:
				pujian = "Aowkaowk."
			self.akhir = tk.Label(self.main_frame, text = pujian+" Skor anda :"+ str(self.skor),font = ('Helvetica', 14, 'bold')).pack(pady=(10,5))

			self.yesno = askyesno(title='confirmation',message='Simpan Skor?')
			if self.yesno:
				self.save_score_label = tk.Label(self.main_frame,text="Masukkan nama :",font = ('Helvetica', 10, 'bold'))
				self.save_score_input = tk.Entry(self.main_frame,font = ('Helvetica', 10, 'bold'))
				self.save_score_button = tk.Button(self.main_frame,text="Submit",font = ('Helvetica', 10, 'bold'),command=self.save_score)

				self.save_score_label.pack(pady=(10,0))
				self.save_score_input.pack()
				self.save_score_button.pack(pady=(5,0))
			else:
				self.retrybtn()

	def save_score(self):
		dataa = {}
		today = date.today()
		tanggal = today.strftime("%B %d, %Y")

		dataa['nickname'] = self.save_score_input.get()
		dataa['score'] = self.skor
		dataa['date'] = tanggal

		try:
			req = requests.post(self.HOSTNAME+'api',data=dataa)
			res = req.json()

			if res['status'] == "Success!":
				self.save_score_input.pack_forget()
				self.save_score_label.pack_forget()
				self.save_score_button.pack_forget()
				self.retrybtn()
			else:
				print("Something Wrong!")

		except:
				self.offline_alert_label = tk.Label(self.main_frame,text="Request timed out. Can't connect to server",fg='red',font = ('Helvetica', 10, 'bold'))
				self.offline_alert_label.pack()
				self.offline_alert_label.after(2000, self.offline)

	def offline(self):		
		self.offline_alert_label.pack_forget()


	def retrybtn(self):
		self.retry_label = tk.Button(self.main_frame,text="Main Lagi",fg='green',font = ('Helvetica', 14, 'bold'),command=self.retry)
		self.retry_label.pack(pady=50)

	def retry(self):
		self.main_frame.destroy()
		Game()

	def showLeaderboard(self):
		self.lb_frame = tk.Tk()
		self.lb_frame.geometry("400x250+0+0")
		self.lb_frame.minsize(400,250)
		self.lb_frame.maxsize(400,250)
		self.lb_frame.title("Leaderboard")

		self.lb_txt = tk.Label(self.lb_frame, text = 'Top 10 Leaderboard',font = ('Helvetica', 13, 'bold')).pack()

		self.getDataLB()

		self.lb_frame.mainloop()

	def getDataLB(self):
		try:
			data_lb = requests.get(self.HOSTNAME+'leaderboard').json()
			self.lb_list_label = []

			c = 0
			for key, value in data_lb.items():
				self.lb_list_label.append(tk.Label(self.lb_frame, text = str(c+1)+". "+ str(data_lb[key][0]) + " :" + str(data_lb[key][1]) + "   ("+ str(data_lb[key][2])+")",font = ('Helvetica', 10)).pack())
				c+=1

		except:
			self.err_label = tk.Label(self.lb_frame, text ="No internet connection",font = ('Helvetica', 10)).pack()

	def nextColor(self):
		if self.durasi > 0 :
			self.input.focus_set()
			if self.input.get().lower() == self.warna[1].lower():
				self.skor += 1
			self.input.delete(0,tk.END)

			random.shuffle(self.warna) 	
			self.warna_label.config(fg = self.warna[1], text = str(self.warna[0]))
			self.skor_label.config(text = "Score: " + str(self.skor))


if __name__ == '__main__':
	Game()