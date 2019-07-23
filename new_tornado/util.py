#! /usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Optional, Type, Dict, Any

class Configurable(object):

	__impl_class = None  # type: Optional[Type[Configurable]]
	__impl_kwargs = None  # type: Dict[str, Any]

	def __new__(cls, *args: Any, **kwargs: Any) -> Any:
		base = cls.configurable_base()
		init_kwargs = dict()
		if cls is base:
			impl = cls.configured_class()
			if base.__impl_kwargs:
				init_kwargs.update(base.__impl_kwargs)
		else:
			impl = cls
		init_kwargs.update(kwargs)
		if impl.configurable_base() is not base:
			return impl(*args, **init_kwargs)
		instance = super(Configurable, cls).__new__(impl)

		instance.initialize(*args, **init_kwargs)
		return instance
	def _initialize(self):
		pass
	initialize = _initialize
	@classmethod
	def configurable_base(cls):

		raise NotImplementedError()

	@classmethod
	def configurable_default(cls):
		raise NotImplementedError()

	@classmethod
	def configured_class(cls):
		# type: () -> Type[Configurable]
		"""Returns the currently configured class."""
		base = cls.configurable_base()
		# Manually mangle the private name to see whether this base
		# has been configured (and not another base higher in the
		# hierarchy).
		if base.__dict__.get("_Configurable__impl_class") is None:
			base.__impl_class = cls.configurable_default()
		if base.__impl_class is not None:
			return base.__impl_class
		else:
			# Should be impossible, but mypy wants an explicit check.
			raise ValueError("configured class not found")

	@classmethod
	def _save_configuration(cls):
		# type: () -> Tuple[Optional[Type[Configurable]], Dict[str, Any]]
		base = cls.configurable_base()
		return (base.__impl_class, base.__impl_kwargs)

if __name__ == '__main__':
	pass