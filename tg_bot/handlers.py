import pandas as pd
import logging
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import Router, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from get_response_model import GPT3, all_step
import asyncio
import openai_async
import os
from dotenv import load_dotenv
import db
from datetime import datetime
import time
import ast
load_dotenv()


menu_router = Router()
choose_model_keyboard = ReplyKeyboardBuilder()
menu = ReplyKeyboardBuilder()

models = ['GPT-3.5', 'All step', 'x25']

choose_model_keyboard.row(
    types.KeyboardButton(text="GPT-3.5"),
    types.KeyboardButton(text="All step")
    )
    
choose_model_keyboard.row(
    types.KeyboardButton(text="x25"),
    types.KeyboardButton(text="Сбросить контекст"),
    )
    
df = pd.read_excel('test.xlsx')
df_dict = {
    "df": df
}
print('запустились')
class SessionState(StatesGroup):
    model = State()
"""
@menu_router.message(F.text.lower() == "mixstral")
async def mixstral(message: types.Message): 
    stdin, stdout, stderr = ssh.exec_command(message.text)
    await message.answer(stdout.read().decode('utf-8'))
"""
    

@menu_router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer(
        text="Выберите модель:",
        reply_markup=choose_model_keyboard.as_markup(resize_keyboard=True)
    )
    await state.set_state(SessionState.model)

@menu_router.message(F.text.in_(models))
async def choose_model(message: types.Message, state: FSMContext):
    session_id = message.chat.id
    db.del_session(session_id)
    await state.update_data(model=message.text)
    await message.answer(f'Выбрана модель: {message.text}')
    
@menu_router.message(F.text.lower() == 'сбросить контекст')
async def del_session(message: types.Message, state: FSMContext):
    session_id = message.chat.id
    db.del_session(session_id)
    await message.answer('Контекст сброшен')
    
@menu_router.message()
async def get_response(message: types.Message, state: FSMContext):   
    request = message.text
    session_id = message.chat.id
    session_state = await state.get_data()
    session = db.get_session(session_id)
    try:
        model = session_state['model']
    except:
        try:
            model = db.get_value(session, 'model')
        except:
            model = 'GPT-3.5'
    
    if model == 'GPT-3.5':
        await GPT3(session_id, session, request)
    
    if model == 'All step':
        await all_step(session_id, session, request, message, df_dict['df'])
    if model == 'x25':
        tasks = [all_step(session_id, session, request, message, df_dict['df']) for _ in range(10)]
        error = 0
        valid = 0
        invalid = 0
        results = await asyncio.gather(*tasks)
        print('закончили')
        for result in results:
            print(result)
            if '295' in result and '274' in result:
                valid += 1
            elif 'Traceback' in result:
                error += 1
            else:
                invalid += 1
                
        await message.answer(f'Valid: {valid}, Error: {error}, Invalid: {invalid}')