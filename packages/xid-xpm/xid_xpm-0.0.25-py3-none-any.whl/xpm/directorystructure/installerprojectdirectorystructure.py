#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
from .projectdirectorystructure import ProjectDirectoryStructure


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
EMPTY: str = ""
SPACE: str = " "
LINEFEED: str = "\n"


#--------------------------------------------------------------------------------
# 인스톨러 프로젝트 디렉토리 구조 클래스.
#--------------------------------------------------------------------------------
class InstallerProjectDirectoryStructure(ProjectDirectoryStructure):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__originRootDirectory: str
	__origins: Dict[str, str]
	__destinationRootDirectory: str
	__destinations: Dict[str, str]


	#--------------------------------------------------------------------------------
	# 소스 루트 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def OriginRootDirectory(thisInstance) -> str:
		return thisInstance.__originRootDirectory
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 루트 디렉토리 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def DestinationRootDirectory(thisInstance) -> str:
		return thisInstance.__destinationRootDirectory


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, destinationRootDirectory: str) -> None:
		base = super()
		base.__init__()
		thisInstance.__originRootDirectory: str = os.path.join(thisInstance.BuildDirectory, "origin")
		thisInstance.__destinationRootDirectory: str = destinationRootDirectory
		thisInstance.__origins: Dict[str, str] = dict()
		thisInstance.__destinations: Dict[str, str] = dict()
		os.makedirs(thisInstance.OriginRootDirectory, exist_ok = True)
		# os.makedirs(thisInstance.DestinationRootDirectory, exist_ok = True)


	#--------------------------------------------------------------------------------
	# 소스 디렉토리 설정.
	#--------------------------------------------------------------------------------
	def SetOrigin(thisInstance, key: str, value: str) -> None:
		thisInstance.__origins[key] = value


	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 설정.
	#--------------------------------------------------------------------------------
	def SetDestination(thisInstance, key: str, value: str) -> None:
		thisInstance.__destinations[key] = value


	#--------------------------------------------------------------------------------
	# 소스 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetOrigin(thisInstance, key: str, defualt: Optional[str] = None) -> Optional[str]:
		return thisInstance.__origins.get(key, defualt)
	
	#--------------------------------------------------------------------------------
	# 소스 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetOrigins(thisInstance) -> ItemsView:
		return thisInstance.__origins.items()
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetDestination(thisInstance, key: str, defualt: Optional[str] = None) -> Optional[str]:
		return thisInstance.__destinations.get(key, defualt)
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 반환.
	#--------------------------------------------------------------------------------
	def GetDestinations(thisInstance) -> ItemsView:
		return thisInstance.__destinations.items()


	#--------------------------------------------------------------------------------
	# 소스 디렉토리의 키 보유 여부 반환.
	#--------------------------------------------------------------------------------
	def HasOrigin(thisInstance, key: str) -> bool:
		return key in thisInstance.__origins
	

	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리의 키 보유 여부 반환.
	#--------------------------------------------------------------------------------
	def HasDestination(thisInstance, key: str) -> bool:
		return key in thisInstance.__destinations
	

	#--------------------------------------------------------------------------------
	# 소스 디렉토리 전체 비우기.
	#--------------------------------------------------------------------------------
	def ClearOrigin(thisInstance) -> None:
		thisInstance.__origins.clear()


	#--------------------------------------------------------------------------------
	# 데스티네이션 디렉토리 전체 비우기.
	#--------------------------------------------------------------------------------
	def ClearDestination(thisInstance) -> None:
		thisInstance.__destinations.clear()