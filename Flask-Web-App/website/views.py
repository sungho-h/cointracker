from threading import Timer
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Wallet, Transaction
from . import db
import json
from urllib.request import urlopen


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        address = request.form.get('address')

        wallets = [w for w in Wallet.query.filter_by(address=address)]
        print(address)
        print("wallets", wallets)
        print()
        if wallets != []:
            flash('wallet already registered', category='error')
            return render_template("home.html", user=current_user)
            

        try:
            with urlopen(f'https://api.blockchair.com/bitcoin/dashboards/address/{address}?transaction_details=true') as res:
                string = res.read().decode('utf-8')
                json_obj = json.loads(string)["data"][address]

                balance = json_obj["address"]["balance"]
                transactions = json_obj["transactions"]
                for t in transactions:
                    new_transaction = Transaction(
                                        wallet_address=address,
                                        balance_change=t["balance_change"],
                                        time=t["time"],
                                        hash=t["hash"]
                                        )
                    db.session.add(new_transaction)
                db.session.add(Wallet(user_id=current_user.id, address=address, balance=balance))
                db.session.commit()
                # flash('new wallet added in successfully!', category='success')
        except:
            flash('invalid btc address', category='error')

    return render_template("home.html", user=current_user)


@views.route('/refresh', methods=['POST'])
def refresh_wallet(user_id=None):
    # note = json.loads(request.data)
    if user_id:
        wallets = Wallet.query.filter_by(user_id=user_id)
    else:
        wallets = Wallet.query.filter_by(user_id=current_user.id)

    for wallet in wallets:
        address = wallet.address
        try:
            with urlopen(f'https://api.blockchair.com/bitcoin/dashboards/address/{address}?transaction_details=true') as res:
                string = res.read().decode('utf-8')
                json_obj = json.loads(string)
                if json_obj["context"] != 200:
                    raise Exception("api call unsuccessful")
                new_balance = json_obj["data"][address]["address"]["balance"]
                # if balance did not change, dont check for new transactions. (need to talk about trade offs)
                if new_balance == wallet.balance:
                    flash(f'detected a change in wallet:{{address}}!', category='success')
                    break

                wallet.balnace = new_balance
                transactions = set([t.hash for t in wallet.transactions])

                new_transactions = json_obj["data"][address]["transactions"]
                for t in new_transactions:
                    if t['hash'] not in transactions:
                        new_transaction = Transaction(
                                            wallet_address=address,
                                            balance_change=t["balance_change"],
                                            time=t["time"],
                                            hash=t["hash"]
                                            )
                        db.session.add(new_transaction)
                db.session.commit()
        except:
            flash('unable to sync wallet data', category='error')
    return render_template("home.html", user=current_user)

def refresh_all_wallet():
    users = User.query.all()
    for user in users:
        refresh_wallet(user.id)


# cron job that runs every 5min (300s) to detect if any change has occurred in the user's wallets
t = Timer(300.0, refresh_all_wallet)
t.start()

